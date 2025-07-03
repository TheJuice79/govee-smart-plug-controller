# Use a minimal official Python image as the base
FROM python:3.11-slim

# --------------------------------------------
# 📌 OCI-compliant image metadata labels
# --------------------------------------------
LABEL maintainer="TheJuice79 <you@example.com>"
LABEL org.opencontainers.image.title="Govee Smart Plug Controller"
LABEL org.opencontainers.image.description="Automates a Govee smart plug based on weather and time window conditions."
LABEL org.opencontainers.image.version="1.1.1"
LABEL org.opencontainers.image.source="https://github.com/TheJuice79/govee-smart-plug-controller"
LABEL org.opencontainers.image.documentation="https://github.com/TheJuice79/govee-smart-plug-controller"
LABEL org.opencontainers.image.licenses="MIT"

# --------------------------------------------
# 📂 Set working directory inside container
# --------------------------------------------
WORKDIR /app

# --------------------------------------------
# 📄 Copy requirements file and install dependencies
# --------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------------
# 📁 Copy all source files into the container
# --------------------------------------------
COPY . .

# --------------------------------------------
# 🏁 Default command to run when the container starts
# You can change 'main.py' to your actual entry point
# --------------------------------------------
CMD ["python", "main.py"]