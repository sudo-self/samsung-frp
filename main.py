from adb_utils import manualFRPBypass, uploadAndRunFRPBypass, waitForDevice
from at_utils import enableADB
from usbswitcher import samsungGalaxyToModemMode


def main():
    print("==== Samsung FRP Bypass Tool ====")
    print("Device model: A03 SM-S135DL")

    # Step 1: Switch to modem mode
    print("\nStep 1: Switching to modem mode...")
    samsungGalaxyToModemMode()

    # Step 2: Enable ADB if needed
    print("\nStep 2: Enabling ADB...")
    enableADB()

    # Step 3: Wait for device
    print("\nStep 3: Waiting for device...")
    waitForDevice()

    # Step 4: Run FRP bypass
    print("\nStep 4: Running FRP bypass...")
    bypass_method = (
        input("Choose FRP bypass method (1=binary, 2=manual, default=1): ") or "1"
    )

    if bypass_method == "2":
        print("Using manual FRP bypass method...")
        manualFRPBypass()
    else:
        print("Using binary FRP bypass method...")
        uploadAndRunFRPBypass()

    print("\nFRP bypass process complete!")


if __name__ == "__main__":
    main()
