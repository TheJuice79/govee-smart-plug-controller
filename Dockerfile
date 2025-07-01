# Use an official Python base image
FROM python:3.11.9-slim-bookworm

# Set environment variable for timezone (default: UTC)
ENV TZ=UTC

# Set working directory
WORKDIR /app

# Install tzdata and Python dependencies
RUN apt-get update && \
    apt-get install -y tzdata && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure the timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy the Python script and requirements
COPY requirements.txt .
COPY controller.py .

# Run the script
CMD ["python", "controller.py"]
