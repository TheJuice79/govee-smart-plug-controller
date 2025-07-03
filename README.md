
# Govee Controller

A Python script and Docker container that automatically controls a Govee smart plug based on weather conditions such as temperature and cloud cover. Ideal for automating pool heaters, fans, or other devices depending on outdoor conditions.

---

## ✅ Features

- Pulls current weather from the Open-Meteo API
- Turns Govee smart plug ON or OFF using configurable thresholds
- Runs on a schedule with graceful shutdown handling
- Deployable via Docker or Docker Compose
- Pushes to GitHub Container Registry for easy Portainer or cloud deployment
- Logs with time zone awareness

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/TheJuice79/govee-smart-plug-controller.git
cd govee-smart-plug-controller
```

### 2. Create a `.env` File

Create a `.env` file in the root directory with your configuration:

```env
GOVEE_API_KEY=your_govee_api_key
DEVICE_MAC=your_device_mac
DEVICE_MODEL=your_device_model
LAT=39.8333
LON=-98.5855
START_TIME=00:00
END_TIME=23:59
TEMP_UNIT=fahrenheit
TEMP_THRESHOLD=75
CLOUD_THRESHOLD=50
CHECK_INTERVAL=15
TZ=America/Chicago
```

---

## 🐳 Using Docker

### Build Locally

```bash
docker build -t govee-controller .
```

### Run

```bash
# From GitHub Container Registry
docker run --env-file .env --restart unless-stopped --name govee-controller ghcr.io/thejuice79/govee-smart-plug-controller:latest

# Or from Docker Hub
docker run --env-file .env --restart unless-stopped --name govee-controller thejuice79/govee-smart-plug-controller:latest
```

---

## 🧱 Using Docker Compose

Create a `docker-compose.yml`:

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
      - LAT=39.8333
      - LON=-98.5855
      - START_TIME=00:00
      - END_TIME=23:59
      - TEMP_UNIT=fahrenheit
      - TEMP_THRESHOLD=75
      - CLOUD_THRESHOLD=50
      - CHECK_INTERVAL=15
      - TZ=America/Chicago
    restart: unless-stopped
```

Then start with:

```bash
docker compose up -d
```

---

## How to Get Your Govee API Key

To control your Govee smart devices programmatically, you need to obtain an API key from Govee. Follow these steps:

1. **Create a Govee Developer Account**  
   - Visit the [Govee Developer Portal](https://developer.govee.com/).  
   - Click **Sign Up** and create a new account using your email address.

2. **Verify Your Email**  
   - Check your email inbox for a verification message from Govee.  
   - Follow the link in the email to verify your account.

3. **Log in to the Developer Portal**  
   - After verification, log in at [https://developer.govee.com/](https://developer.govee.com/).

4. **Create a New API Key**  
   - Navigate to the **API Keys** section in your dashboard.  
   - Click **Create API Key**.  
   - Provide a name/label for your key (e.g., "Govee Controller Script").  
   - Agree to the terms and generate the key.

5. **Copy Your API Key**  
   - Copy the generated API key to your clipboard.  
   - Keep this key safe and **do not share it publicly**.

6. **Add the API Key to Your `.env` File**  
   - Open your `.env` file in the project directory.  
   - Set the `GOVEE_API_KEY` variable to your copied API key, like this:  
     ```env
     GOVEE_API_KEY=your_actual_govee_api_key_here
     ```

---

## How to Find Your Govee Device MAC Address and Model Number

You need the **MAC address** and **model number** of your Govee smart plug to configure the controller correctly. Here's how to find them:

### Option 1: Using the Govee Home App

1. Open the **Govee Home** app on your smartphone.
2. Navigate to your smart plug device in the device list.
3. Tap on the device to open its settings.
4. Scroll down to find **Device Information** or **About**.
5. Look for the **MAC Address** and **Model Number** listed there.
6. Note these values exactly as shown (usually MAC looks like `A1:B2:C3:D4:E5:F6`).

### Option 2: Using the Govee API (Requires API Key)

You can list your devices with the Govee API to get their MAC and model info:

```bash
curl -H "Govee-API-Key: YOUR_API_KEY" https://developer-api.govee.com/v1/devices
```

This returns JSON with your registered devices and their details, including `device` (MAC) and `model`.

---

## 🛠 Environment Variables

| Variable         | Required | Description                                                                 |
|------------------|----------|-----------------------------------------------------------------------------|
| `GOVEE_API_KEY`  | ✅       | Your Govee API key from [developer.govee.com](https://developer.govee.com/) |
| `DEVICE_MAC`     | ✅       | MAC address of the Govee plug (format: `AA:BB:CC:DD:EE:FF`)                 |
| `DEVICE_MODEL`   | ✅       | Model number of the Govee plug (e.g., `H5083`)                              |
| `LAT`            | ✅       | Latitude of your location (e.g., `44.2760`)                                 |
| `LON`            | ✅       | Longitude of your location (e.g., `-88.2724`)                               |
| `START_TIME`     | ❌       | The earliest time of day (in `HH:MM` 24-hour format) to allow plug control. |
| `END_TIME  `     | ❌       | The latest time of day (in `HH:MM` 24-hour format) to allow plug control.   |
| `TEMP_UNIT     ` | ❌       | Temperature unit for weather API: "fahrenheit" or "celsius" (default: `fahrenheit`) |
| `TEMP_THRESHOLD` | ❌       | Temperature in °F above which the plug turns ON (default: `75`)             |
| `CLOUD_THRESHOLD`| ❌       | Cloud cover percentage below which the plug turns ON (default: `50`)        |
| `CHECK_INTERVAL` | ❌       | Time between weather checks, in minutes (default: `15`)                     |
| `TZ`             | ❌       | Time zone for logging/scheduling (e.g., `America/Chicago`). [See full list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

## 📦 GitHub Container Registry (GHCR)

Image is available here:

```
ghcr.io/thejuice79/govee-smart-plug-controller:latest
```

You can pull and run it anywhere with:

```bash
docker pull ghcr.io/thejuice79/govee-smart-plug-controller:latest
```

---

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

---

## Author

[TheJuice79](https://github.com/TheJuice79)

---

## 📋 Changelog

### [v1.2.1] - 2025-07-03
- Restructured project layout into `/app` package with `__init__.py`.
- Fixed `ModuleNotFoundError: No module named 'app'` by ensuring relative imports align with package layout.
- Updated Dockerfile `WORKDIR` and CMD path to use `/app/main.py`.
- Modified test files and `PYTHONPATH` to resolve module import errors during test runs.
- Added `.env` parsing improvements: trims whitespace and supports inline comments.
- Updated GitHub Actions CI to reflect new file structure and paths.
- Updated Makefile to support builds from `./docker` folder.
- Updated GitHub and Docker Hub documentation to match.

### [v1.2.0] - 2025-07-02
- Added time window logic with `START_TIME` and `END_TIME` environment variables.
- Refactored core logic into modular components: `scheduler.py`, `config.py`, `controller.py`, etc.
- Added retry logic to API requests using `tenacity`.
- Introduced automated testing via `pytest` and monkeypatch-based mocks.
- Created a `Makefile` with targets for `build`, `test`, `push`, and `publish`.
- Added GitHub Actions CI for push events.

### [v1.1.1] - 2025-07-01
- Allowed setting timezone via the `TZ` environment variable.
- Converted script to log server-local time correctly inside the container.
- Changed default Docker image base to `python:3.11-slim`.
- Published image to both Docker Hub and GitHub Container Registry (`ghcr.io`).
- Updated `README.md` with improved Docker and Portainer deployment instructions.

### [v1.0.0] - Initial Release
- Core Govee plug control logic using Open-Meteo weather data.
- Temperature and cloud cover thresholds trigger plug ON/OFF.
- Supports Docker deployment and `.env` config.


---

## 🛠 Makefile Support

This project includes a `Makefile` to simplify common Docker operations:

```bash
make build    # Build Docker image
make test     # Run Python tests
make publish  # Build and push image to registry
```

---

## 🔗 Additional Resources

- [Releases](https://github.com/TheJuice79/govee-smart-plug-controller/releases)
- [Issues](https://github.com/TheJuice79/govee-smart-plug-controller/issues)
