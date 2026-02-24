import subprocess
import yaml
import requests
import time

CONFIG_PATH = "/etc/tesseract/config/config.yaml"

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

BOT_TOKEN = cfg['telegram']['bot_token']
CHAT_ID = cfg['telegram']['chat_id']
SERVICES = cfg.get('services', [])
CHECK_INTERVAL = cfg.get('check_interval', 60)
GLOBAL_AUTORESTART = cfg.get('autorestart', False)
SERVICE_SLEEP = cfg.get('service_sleep', 0.5)  # seconds to wait between services

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except Exception as e:
        print("Failed to send alert:", e)

def check_service(service_name):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True, text=True, timeout=5
        )
        status = result.stdout.strip()
    except subprocess.TimeoutExpired:
        status = "unknown"

    if status != "active":
        if GLOBAL_AUTORESTART:
            send_alert(f"Tesseract Alert: Service {service_name} is down, attempting restart...")
            try:
                subprocess.run(["systemctl", "restart", service_name], timeout=10)
            except subprocess.TimeoutExpired:
                send_alert(f"Tesseract Alert: Service {service_name} restart timed out ❌")

            # check again
            try:
                result = subprocess.run(
                    ["systemctl", "is-active", service_name],
                    capture_output=True, text=True, timeout=5
                )
                status = result.stdout.strip()
            except subprocess.TimeoutExpired:
                status = "unknown"

            if status == "active":
                send_alert(f"Tesseract Alert: Service {service_name} has been restored ✅")
            else:
                send_alert(f"Tesseract Alert: Service {service_name} is still down ❌")
        else:
            send_alert(f"Tesseract Alert: Service {service_name} is down ❌")

if __name__ == "__main__":
    while True:
        for svc in SERVICES:
            check_service(svc)
            time.sleep(SERVICE_SLEEP)  # short pause between services
        time.sleep(CHECK_INTERVAL)