# 📋 Changelog

All notable changes for each version are listed below.

---
## [v1.5.2] - 2025-07-21

### ✨ Added
- `force` parameter to plug control methods, enabling forced state resets before sending ON/OFF commands.
- Improved weather API fallback logic: if WeatherAPI fails, the system gracefully falls back to Open-Meteo for reliable data.

### 🔧 Changed
- `PlugScheduler` now uses the new `force` option to ensure more robust plug control during uncertain or inconsistent states.

### 🛠️ Improvements
- Enhanced resilience when fetching weather data, ensuring more consistent automation behavior even during intermittent API failures.

This update improves both plug command reliability and weather data robustness for smarter automation.

---

## [1.5.1] – 2025‑07‑08
### 🧼 Internal Refactor
- Split `fetch_weather()` into a new `weather.py` module
- Moved scheduling logic (`run_loop`, `sleep_until_next_start`) to `scheduler.py`
- Updated test suite:
  - `test_scheduler.py` for scheduling logic
  - `test_weather.py` for weather API logic
- No changes to external behavior or config required

---

## [1.5.0] – 2025‑07‑08
### ✨ New Features
- Added support for fallback to Open-Meteo API when `WEATHERAPI_KEY` is not provided
- Updated `fetch_weather()` to switch dynamically between WeatherAPI and Open-Meteo
- Maintains full backward compatibility with earlier `.env` files
- Extended unit tests to verify both WeatherAPI and Open-Meteo behavior

---

## [1.4.3] – 2025‑07‑08
### 🔄 Changed
- Replaced Open-Meteo API with WeatherAPI for better real-time temperature and cloud accuracy
- Updated `fetch_weather()` to support WeatherAPI's format
- Modified `.env` example and README with `WEATHERAPI_KEY`
- Adjusted tests and mocking to reflect WeatherAPI response format

---

## [1.4.2] – 2025‑07‑07
### 🛠 Bug Fixes
- Ensured `turn_off_plug()` is called when outside the configured `START_TIME`–`END_TIME` window to prevent pump from staying on.
- Updated `test_run_loop_outside_time` to mock `Controller` and assert that `turn_off_plug()` is invoked correctly during off-hours.

---

## [1.4.1] – 2025‑07‑06
### 🛠 Bug Fixes
- Added a defensive check to ensure instance methods like `send_command()` and `turn_off_plug()` are **only called on a `Controller` instance**.
- Prevents ambiguous `AttributeError` when methods are mistakenly called via the class.
- Enhanced test coverage with a specific case validating proper instance method usage.

---

## [1.4.0] – 2025‑07‑06
### ✨ New Features
- Introduced `Controller` class with **state caching** to avoid redundant API calls.
- Added validation to accept only `"on"` or `"off"` commands.
- Enhanced unit tests for controller logic, including:
  - State transitions (`on` → `off`, `off` → `on`)
  - API skipping behavior
  - Input validation
  - Request retry logic

### 🔄 Changes
- Made `send_command()`, `turn_on_plug()`, and `turn_off_plug()` instance methods.
- `send_command()` now validates commands and logs more precisely.

### 🐞 Fixes
- Invalid commands no longer update internal state or trigger API calls.

---

## [1.3.2] – 2025‑07‑03
### 🐞 Fixes
- Resolved Docker container startup error caused by incorrect path to `main.py`.

---

## [1.3.1] – 2025‑07‑03
### 🧪 Improvements
- Added pytest coverage for scheduler and config logic.
- Fixed temperature unit handling in `fetch_weather()`.

---

## [1.3.0] – 2025‑07‑03
### ✨ New Features
- Added support and validation for `TEMP_UNIT` (Fahrenheit/Celsius).
- Improved scheduling using `sleep_until_next_start()`.

---

## [1.2.1] – 2025‑07‑02
### 🧩 Refactor
- Modularized code into an `/app` package.
- Fixed import issues and cleaned up Dockerfile.

---

## [1.2.0] – 2025‑07‑02
### ✨ New Features
- Introduced time window control with `START_TIME`/`END_TIME`.
- Added retry logic using `tenacity`.
- Created `Makefile` and added GitHub Actions CI for streamlined development.

---

## [1.1.1] – 2025‑07‑01
### ✨ New Features
- Added timezone support for proper logging.
- Enabled Docker image publishing.

---

## [1.0.0] – 2025‑07‑01
### ✨ Initial Release
- Automated Govee smart plug based on outdoor weather (temperature, cloud cover).
