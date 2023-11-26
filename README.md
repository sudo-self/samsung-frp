# Samsung FRP Bypass
- Make sure you have all the dependencies listed in `requirements.txt` installed
  - Install them using `pip install -r requirements.txt`
- You can simply plug the samsung over USB and run `python main.py`


FRP.BIN
<img width="802" alt="Screenshot 2023-11-26 at 1 33 41 AM" src="https://github.com/sudo-self/frp-linux/assets/119916323/eb2e4ae8-a0ad-4a7a-9ce9-f815de1eea09">



settings put global setup_wizard_has_run 1<br>
settings put secure user_setup_complete 1<br>
content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1<br>
content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1<br>
content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1<br>
am start -c android.intent.category.HOME -a android.intent.action.MAINbr>
Wait 5 sec<br>
am start -n com.android.settings/com.android.settings.Settings<br>
Wait 5 sec<br>
reboot
