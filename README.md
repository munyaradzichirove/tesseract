# Tesseract – Systemd Watchdog with Telegram Alerts

Tesseract is a **lightweight Python-based watchdog** that monitors your systemd services and sends **Telegram alerts** if any of them stop. It’s designed to run as a **persistent background service** using systemd, fully configurable via YAML.

---

## Features

* Monitor multiple systemd services defined in a YAML config
* Telegram alerts on service failure
* Configurable check intervals
* Easy setup using a Bash installer
* Logs service activity (optional)

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/munyaradzichirove/tesseract.git
cd tesseract
```

2. Run the setup script (requires sudo):

```bash
sudo bash setup.sh
```

This will:

* Create `/etc/tesseract` folder structure (`config`, `scripts`, `venv`, `logs`)
* Copy `tesseract.py` and `config.yaml`
* Create a Python virtual environment in `/etc/tesseract/venv` and install dependencies
* Create systemd units: `tesseract.service` and `tesseract.timer`
* Start the service and timer

---

## Configuration

Edit the YAML config file at:

```
/etc/tesseract/config/config.yaml
```

Example:

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  chat_id: "YOUR_CHAT_ID"

services:
  - nginx
  - tesseract
  - postgresql

check_interval: 60  # seconds
```

* `services` → list of systemd services to monitor
* `check_interval` → time between checks

---

## Usage

* **Start / Stop service manually**:

```bash
sudo systemctl start tesseract.service
sudo systemctl stop tesseract.service
```

* **Check status**:

```bash
sudo systemctl status tesseract.service
```

* **View timer status**:

```bash
sudo systemctl list-timers tesseract.timer
```

---

## How it works

1. `tesseract.service` runs the Python script using the virtual environment.
2. Script checks all services listed in the YAML config.
3. If a service is down, Tesseract sends a Telegram message.
4. Systemd automatically restarts the service if it crashes.
5. `tesseract.timer` can be used to trigger the service periodically.

---

## Requirements

* Linux system with systemd
* Python 3.10+
* Telegram bot (create one via BotFather)

---

## Folder structure

```
/etc/tesseract/
├── config/
│   └── config.yaml
├── scripts/
│   └── tesseract.py
├── venv/
├── logs/
└── setup.sh
```

---

## Author

**Munyaradzi Chirove**
Tesseract – Telegram Watchdog for systemd services

---

## License

MIT License

---
