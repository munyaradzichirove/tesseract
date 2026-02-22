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

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def check_service(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True, text=True
    )
    status = result.stdout.strip()

    if status != "active":
        if GLOBAL_AUTORESTART:
            send_alert(f"Tesseract Alert: Service {service_name} is down, attempting restart...")
            subprocess.run(["systemctl", "restart", service_name])
            # check again
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True, text=True
            )
            status = result.stdout.strip()
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
        time.sleep(CHECK_INTERVAL)