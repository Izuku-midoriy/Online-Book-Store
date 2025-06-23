# Use a minimal Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Use gunicorn to serve the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
