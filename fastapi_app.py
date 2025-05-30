# fastapi_app.py
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
import uuid

from agents.classifier_agent import classify_input
from agents.email_parser_agent import parse_email
from agents.json_agent import parse_json_file
from agents.pdf_agent import parse_pdf_invoice
from memory.shared_memory import store_entry, get_all_entries

app = FastAPI(title="Flowbit AI Agent System")

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    file_id = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, file_id)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Classify the uploaded file
    classified = classify_input(file_path)
    format_type = classified["format"]
    intent = classified["intent"]

    # Route to appropriate agent
    try:
        if format_type == "Email":
            parsed = parse_email(classified["content_preview"])

        elif format_type == "JSON":
            parsed = parse_json_file(file_path)

        elif format_type == "PDF":
            parsed = parse_pdf_invoice(file_path)

        else:
            return JSONResponse(content={"error": "Unsupported file format"}, status_code=400)

        # Store in memory
        store_entry(
            source_type=file_path,
            format_type=format_type,
            intent=intent,
            extracted_data=parsed
        )

        return RedirectResponse(url="/?success=true", status_code=303)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/memory/")
def get_memory():
    return {"entries": get_all_entries()}


from fastapi.responses import FileResponse
from memory.shared_memory import export_memory_to_file

@app.get("/export/")
def download_memory():
    path = export_memory_to_file()
    return FileResponse(path, filename="output_logs.json", media_type="application/json")
@app.get("/view-memory", response_class=HTMLResponse)
def view_memory(request: Request):
    entries = get_all_entries()
    return templates.TemplateResponse("memory_view.html", {"request": request, "entries": entries})
