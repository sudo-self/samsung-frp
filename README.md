# Samsung FRP Bypass

- grab python from <a href="https://www.python.org/downloads/">here</a><br>
- Make sure you have all the dependencies listed in `requirements.txt` installed
- Install them using `pip install -r requirements.txt`
- You can simply plug the samsung over USB and run `python main.py`

## unlock.sh

execute_adb_command() {
    adb shell "$1"
}

### Run ADB commands
execute_adb_command "settings put global setup_wizard_has_run 1"
execute_adb_command "settings put secure user_setup_complete 1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1"
execute_adb_command "am start -c android.intent.category.HOME -a android.intent.action.MAIN"

### Wait for 5 seconds
sleep 5

execute_adb_command "am start -n com.android.settings/com.android.settings.Settings"

### Wait for 5 seconds
sleep 5

### Reboot the device
execute_adb_command "reboot"


### main.py

<img width="511" alt="Screenshot 2023-11-26 at 1 46 06 AM" src="https://github.com/sudo-self/samsung-frp/assets/119916323/001dfba7-4941-4d61-828c-da7c0d010f08">
<img width="680" alt="Screenshot 2023-11-26 at 4 20 27 AM" src="https://github.com/sudo-self/samsung-frp/assets/119916323/bd0c81ea-1416-4c21-bbea-c8c382589115">
<br><table style="height: 336px; width: 100%; border-collapse: collapse; background-color: #fcfcfc;"><tbody><tr style="height: 22px;"><td style="width: 76.5326%; height: 22px;"><br><a href="https://bucket.jessejesse.com/android.html">Android Resources</a>
