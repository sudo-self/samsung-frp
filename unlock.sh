#!/bin/bash

# Function to execute ADB commands
execute_adb_command() {
    adb shell "$1"
}

# Run ADB commands
execute_adb_command "settings put global setup_wizard_has_run 1"
execute_adb_command "settings put secure user_setup_complete 1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1"
execute_adb_command "content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1"
execute_adb_command "am start -c android.intent.category.HOME -a android.intent.action.MAIN"

# Wait for 5 seconds
sleep 5

execute_adb_command "am start -n com.android.settings/com.android.settings.Settings"

# Wait for 5 seconds
sleep 5

# Reboot the device
execute_adb_command "reboot"
