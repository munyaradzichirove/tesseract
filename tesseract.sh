#!/bin/bash

cat << "EOF"
  _______ ______  _____ _____ ______ _____            _____ _______ 
 |__   __|  ____|/ ____/ ____|  ____|  __ \     /\   / ____|__   __|
    | |  | |__  | (___| (___ | |__  | |__) |   /  \ | |       | |   
    | |  |  __|  \___ \\___ \|  __| |  _  /   / /\ \| |       | |   
    | |  | |____ ____) |___) | |____| | \ \  / ____ \ |____   | |   
    |_|  |______|_____/_____/|______|_|  \_\/_/    \_\_____|  |_|   
                                                                    
                                                                                                                                                                                                                                                                                    

EOF

BASE_DIR="/etc/tesseract"
ENV_DIR="$BASE_DIR/venv"

mkdir -p "$BASE_DIR/config"
mkdir -p "$BASE_DIR/scripts"
mkdir -p "$ENV_DIR"
mkdir -p "$BASE_DIR/logs"

cp ./config.yaml "$BASE_DIR/config/config.yaml"
cp ./tesseract.py "$BASE_DIR/scripts/tesseract.py"

python3 -m venv "$ENV_DIR"
source "$ENV_DIR/bin/activate"
pip install --upgrade pip
pip install pyyaml requests
deactivate

echo "Tesseract setup complete!"
echo "Folder structure:"
ls -R "$BASE_DIR"
echo "Python virtual environment created in $ENV_DIR with pyyaml and requests installed."

BASE_DIR="/etc/tesseract"
ENV_DIR="$BASE_DIR/venv"
SCRIPT="$BASE_DIR/scripts/tesseract.py"
SERVICE_NAME="tesseract"
SYSTEMD_DIR="/etc/systemd/system"


if [ -f "$SYSTEMD_DIR/$SERVICE_NAME.service" ]; then
    sudo systemctl stop $SERVICE_NAME.service
    sudo systemctl disable $SERVICE_NAME.service
    sudo rm "$SYSTEMD_DIR/$SERVICE_NAME.service"
fi

if [ -f "$SYSTEMD_DIR/$SERVICE_NAME.timer" ]; then
    sudo systemctl stop $SERVICE_NAME.timer
    sudo systemctl disable $SERVICE_NAME.timer
    sudo rm "$SYSTEMD_DIR/$SERVICE_NAME.timer"
fi

cat << EOF | sudo tee "$SYSTEMD_DIR/$SERVICE_NAME.service"
[Unit]
Description=Tesseract Watchdog Service
After=network.target

[Service]
Type=simple
ExecStart=$ENV_DIR/bin/python3 $SCRIPT
WorkingDirectory=$BASE_DIR
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=tesseract

[Install]
WantedBy=multi-user.target
EOF

cat << EOF | sudo tee "$SYSTEMD_DIR/$SERVICE_NAME.timer"
[Unit]
Description=Runs Tesseract service every minute

[Timer]
OnBootSec=10sec
OnUnitActiveSec=10sec
Unit=$SERVICE_NAME.service

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service
sudo systemctl start $SERVICE_NAME.service
sudo systemctl enable $SERVICE_NAME.timer
sudo systemctl start $SERVICE_NAME.timer

echo "Tesseract service and timer installed and running!"


cat << "EOF"
=====================================================
=                                                   =
=          Thank you for using Tessaract            =
=       Brought to you by Munyaradzi Chirove        =
=  https://github.com/munyaradzichirove/tesseract   =
=                                                   =
=====================================================                                                                                                                                                                                                                                                                               

EOF