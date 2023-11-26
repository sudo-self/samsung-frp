# Samsung FRP Bypass
- Make sure you have all the dependencies listed in `requirements.txt` installed
  - Install them using `pip install -r requirements.txt`
- You can simply plug the samsung over USB and run `python main.py`


FRP.BIN
,,,
settings put global setup_wizard_has_run 1
settings put secure user_setup_complete 1
content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1
content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1
content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1
am start -c android.intent.category.HOME -a android.intent.action.MAIN
,,,
Wait 5 sec
,,,
am start -n com.android.settings/com.android.settings.Settings
,,,
Wait 5 sec
reboot

