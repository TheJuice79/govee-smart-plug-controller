# Govee Smart Plug Controller

A Python script and Docker container that automatically controls a Govee smart plug based on outdoor weather conditions such as temperature and cloud cover. Ideal for automating pool heaters, fans, or other weather-sensitive devices.

---

## ✅ Features

- Pulls current weather data from the [WeatherAPI](https://www.weatherapi.com/)
- Automatically turns Govee smart plug ON/OFF based on temperature and cloud cover thresholds
- Avoids redundant API calls by caching the plug state
- Respects configurable time window (`START_TIME` to `END_TIME`)
- Retries API calls gracefully using `tenacity`
- Fully configurable via `.env` file or Docker Compose
- Lightweight Docker and GitHub Container Registry (GHCR) support
- Graceful shutdown handling
- Full unit test coverage

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/TheJuice79/govee-smart-plug-controller.git
cd govee-smart-plug-controller
```

### 2. Create a `.env` File

```env
GOVEE_API_KEY=your_govee_api_key
DEVICE_MAC=your_device_mac
DEVICE_MODEL=your_device_model
LAT=39.8333
LON=-98.5855
START_TIME=09:00
END_TIME=18:00
TEMP_UNIT=fahrenheit
TEMP_THRESHOLD=75
CLOUD_THRESHOLD=50
CHECK_INTERVAL=15
TZ=America/Chicago
WEATHERAPI_KEY=your_weatherapi_key
```

---

## 🐳 Docker Usage

### Run from GHCR

```bash
docker run --env-file .env --restart unless-stopped --name govee-controller   ghcr.io/thejuice79/govee-smart-plug-controller:latest
```

### Run from Docker Hub

```bash
docker run --env-file .env --restart unless-stopped --name govee-controller   thejuice79/govee-smart-plug-controller:latest
```

### Build Locally

```bash
docker build -t govee-controller .
docker run --env-file .env --restart unless-stopped govee-controller
```

---

## 🧱 Docker Compose

```yaml
version: '3.8'

services:
  govee-controller:
    container_name: govee-controller
    image: ghcr.io/thejuice79/govee-smart-plug-controller:latest
    environment:
      - GOVEE_API_KEY=your_govee_api_key
      - DEVICE_MAC=your_device_mac
      - DEVICE_MODEL=your_device_model
      - WEATHERAPI_KEY=your_weatherapi_key
      - LAT=39.8333
      - LON=-98.5855
      - START_TIME=09:00
      - END_TIME=18:00
      - TEMP_UNIT=fahrenheit
      - TEMP_THRESHOLD=75
      - CLOUD_THRESHOLD=50
      - CHECK_INTERVAL=15
      - TZ=America/Chicago
    restart: unless-stopped
```

Start it with:

```bash
docker compose up -d
```

---

## 🔑 How to Get Your Govee API Key

1. Sign up at [https://developer.govee.com](https://developer.govee.com)
2. Verify your email and log in
3. Navigate to the **API Keys** section
4. Create a new API key (e.g., "Pool Heater Controller")
5. Copy and paste it into your `.env` file

---

## 🌦 How to Get a WeatherAPI Key

1. Sign up at [https://www.weatherapi.com](https://www.weatherapi.com)
2. Go to your [API keys dashboard](https://www.weatherapi.com/my/)
3. Copy your free key (e.g., `abcd1234efgh5678`)
4. Add it to your `.env` file as `WEATHERAPI_KEY=your_key_here`

---

## 📡 How to Find Your Govee Plug MAC and Model

### Option 1: Govee Home App
- Open the app and select your device
- Tap "Settings" → "Device Info"
- Note the **MAC address** and **Model Number**

### Option 2: Use the Govee API

```bash
curl -H "Govee-API-Key: YOUR_API_KEY" https://developer-api.govee.com/v1/devices
```

Look for the `device` and `model` fields in the response JSON.

---

## 🧪 Tests

Run all unit tests with:

```bash
make test
# or
pytest tests/
```

Tests include:
- Plug state transitions and caching
- Redundant command suppression
- Command validation
- Retry behavior for failed requests

---

## 📋 Environment Variables

| Variable          | Required | Description                                                                 |
|-------------------|----------|-----------------------------------------------------------------------------|
| `GOVEE_API_KEY`   | ✅       | Your Govee API key from [developer.govee.com](https://developer.govee.com/) |
| `DEVICE_MAC`      | ✅       | MAC address of the Govee plug (e.g., `AA:BB:CC:DD:EE:FF`)                   |
| `DEVICE_MODEL`    | ✅       | Govee plug model number (e.g., `H5083`)                                     |
| `WEATHERAPI_KEY`  | ✅       | Your API key from [weatherapi.com](https://www.weatherapi.com/)             |
| `LAT`             | ✅       | Latitude of your location                                                   |
| `LON`             | ✅       | Longitude of your location                                                  |
| `START_TIME`      | ❌       | Time of day to begin plug control (e.g., `09:00`)                           |
| `END_TIME`        | ❌       | Time of day to stop plug control (e.g., `18:00`)                            |
| `TEMP_UNIT`       | ❌       | `"fahrenheit"` or `"celsius"` (default: `fahrenheit`)                       |
| `TEMP_THRESHOLD`  | ❌       | Temperature above which the plug turns ON (default: `75`)                   |
| `CLOUD_THRESHOLD` | ❌       | Cloud cover below which the plug turns ON (default: `50`)                   |
| `CHECK_INTERVAL`  | ❌       | Minutes between weather checks (default: `15`)                              |
| `TZ`              | ❌       | Timezone (e.g., `America/Chicago`)                                          |

---

## 🧰 Makefile Support

```bash
make build     # Build the Docker image
make test      # Run unit tests
make publish   # Push image to GitHub Container Registry
```

---

## 📦 GitHub Container Registry

Image:  
```
ghcr.io/thejuice79/govee-smart-plug-controller:latest
```

---

## 📋 Changelog

### [1.4.3] – 2025‑07‑08
#### 🔄 Changed
- Replaced Open-Meteo API with WeatherAPI for improved real-time accuracy
- Updated `fetch_weather()` to support WeatherAPI cloud and temperature fields
- Adjusted `.env`, README, and environment variable documentation
- Updated tests to reflect new API format

---

For the full changelog, [click here](https://github.com/TheJuice79/govee-smart-plug-controller/blob/main/CHANGELOG.md).

---

## 🧑‍💻 Author

Developed by [TheJuice79](https://github.com/TheJuice79)

---

## 📝 License

Licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)