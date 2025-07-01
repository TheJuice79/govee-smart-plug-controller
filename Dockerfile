# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the Python script and requirements
COPY requirements.txt .
COPY controller.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "controller.py"]