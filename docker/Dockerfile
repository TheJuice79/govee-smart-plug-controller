# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project source files
COPY . /app/

# Set Python path so 'app' module is found
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "app/main.py"]
