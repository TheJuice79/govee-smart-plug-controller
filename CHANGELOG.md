# 📋 Changelog

All notable changes for each version are listed below.

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
