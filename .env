# Use an official Python base image
FROM python:3.11.9-slim-bookworm

# Set environment variable for timezone (can be overridden via Docker Compose)
ENV TZ=UTC

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install tzdata and Python dependencies
RUN apt-get update && \
    apt-get install -y tzdata && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy remaining app files
COPY controller.py .

# Configure the timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Run the script
CMD ["python", "controller.py"]