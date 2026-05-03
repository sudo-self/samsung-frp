# Samsung FRP Bypass

[![Build Samsung FRP Tool](https://github.com/sudo-self/samsung-frp/actions/workflows/python-package-uv.yml/badge.svg)](https://github.com/sudo-self/samsung-frp/actions/workflows/python-package-uv.yml)

Bypass Factory Reset Protection on Samsung Galaxy devices via ADB and AT serial commands. Includes a PyQt5 GUI and a shell script.

## Requirements

- [Python 3.10+](https://www.python.org/downloads/)
- Dependencies from `requirements.txt`

```bash
pip install -r requirements.txt
```

```
PyQt5
pyserial
pyusb
```

## GUI — frp.py

Plug your Samsung device in over USB and launch:

```bash
python frp.py
```

<img width="1012" alt="Samsung FRP Tool GUI" src="https://github.com/user-attachments/assets/4936974d-81a6-48e7-9b8b-98cf65b633a0" />

Four tabs — USB mode switcher, ADB/AT commands, FRP bypass, and GSM SMS — all running in background threads with a live terminal console.

---

## unlock.sh

```bash
git clone https://github.com/sudo-self/samsung-frp.git
cd samsung-frp
chmod +x unlock.sh
./unlock.sh
```

### ADB command sequence

```bash
execute_adb_command "settings put global setup_wizard_has_run 1"
execute_adb_command "settings put secure user_setup_complete 1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1"
execute_adb_command "am start -c android.intent.category.HOME -a android.intent.action.MAIN"
```

Wait 5 seconds, then:

```bash
execute_adb_command "am start -n com.android.settings/com.android.settings.Settings"
```

Wait 5 seconds — go to **Backup and reset → Factory data reset** — then reboot.

---

## Build — macOS .app

```bash
pyinstaller --onedir --windowed --name "SamsungFRPTool" \
  --hidden-import usb.backend.libusb1 \
  --hidden-import usb.backend.libusb0 \
  --hidden-import serial.tools.list_ports \
  --add-binary "/opt/homebrew/lib/libusb-1.0.dylib:." \
  --strip \
  --exclude-module matplotlib \
  --exclude-module numpy \
  --exclude-module pandas \
  --exclude-module PIL \
  --exclude-module tkinter \
  --exclude-module unittest \
  --noconfirm \
  frp.py
```

Output: `dist/SamsungFRPTool.app`

---






