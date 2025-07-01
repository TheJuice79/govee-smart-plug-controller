
# Govee Controller

A Python script and Docker container that automatically controls a Govee smart plug based on weather conditions such as temperature and cloud cover. Ideal for automating pool heaters, fans, or other devices depending on outdoor conditions.

---

## Features

- Fetches temperature and cloud cover from the Open-Meteo API.
- Turns Govee smart plug ON or OFF based on user-configurable thresholds.
- Runs continuously with configurable check intervals.
- Gracefully handles shutdown signals to turn off the plug.
- Configurable via environment variables, suitable for Docker deployment.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- Govee smart plug and Govee API key

### Setup

1. Clone this repository:

```bash
git clone https://github.com/TheJuice79/govee-controller.git
cd govee-controller
```

2. Create a `.env` file in the project root and add your configuration:

```env
GOVEE_API_KEY=your_govee_api_key_here
DEVICE_MAC=your_device_mac_address_here
DEVICE_MODEL=your_device_model_here
LAT=39.828
LON=-98.580
TEMP_THRESHOLD=75
CLOUD_THRESHOLD=50
CHECK_INTERVAL=15
```

3. Run the script locally:

```bash
pip install -r requirements.txt
python govee_controller.py
```

4. (Optional) Build and run with Docker:

```bash
docker build -t govee-controller .
docker run --env-file .env govee-controller
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

## Environment Variables

| Variable        | Description                              | Default       |
|-----------------|------------------------------------------|---------------|
| GOVEE_API_KEY   | Your Govee API key                       | (required)    |
| DEVICE_MAC      | MAC address of your Govee device         | (required)    |
| DEVICE_MODEL    | Model number of your Govee device        | (required)    |
| LAT             | Latitude for weather API                 | Required      |
| LON             | Longitude for weather API                | Required      |
| TEMP_THRESHOLD  | Temperature °F threshold to turn ON plug | 75            |
| CLOUD_THRESHOLD | Cloud cover % threshold to turn ON plug  | 50            |
| CHECK_INTERVAL  | Minutes between weather checks           | 15            |

---

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

---

## Author

[TheJuice79](https://github.com/TheJuice79)
