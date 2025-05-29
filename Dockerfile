# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Create upload and output folders (just in case)
RUN mkdir -p data/sample_input data/sample_output data/uploads

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
