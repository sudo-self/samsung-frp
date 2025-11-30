import usb.backend.libusb0
import usb.backend.libusb1
import usb.core

# ---------------------------------------------------------------------------
# USB Backend Setup
# ---------------------------------------------------------------------------

try:
    # Preferred backend: libusb-1.0
    backend = usb.backend.libusb1.get_backend(
        find_library=lambda _: "/opt/homebrew/lib/libusb-1.0.dylib"
    )

    if backend is None:
        # Fallback backend: libusb-0.x
        backend = usb.backend.libusb0.get_backend(
            find_library=lambda _: "/opt/homebrew/lib/libusb.dylib"
        )

except Exception as e:
    print(f"Warning: Error setting USB backend: {e}")
    backend = None


# ---------------------------------------------------------------------------
# Samsung USB Constants
# ---------------------------------------------------------------------------

SAMSUNG_GALAXY_ID_VENDOR = 0x04E8
SAMSUNG_GALAXY_ID_PRODUCT = 0x6860

USB_MODEM_CONFIGURATION = 0x2


# ---------------------------------------------------------------------------
# USB Configuration Helpers
# ---------------------------------------------------------------------------

def setUSBConfig(dev: usb.core.Device, config: int) -> bool:
    """Attempt to set the USB configuration of the device."""
    try:
        dev.reset()
        dev.set_configuration(config)
    except usb.core.USBError as e:
        print(f"USB configuration error: {e}")
        return False

    return True


# ---------------------------------------------------------------------------
# Main Samsung Modem Mode Logic
# ---------------------------------------------------------------------------

def samsungGalaxyToModemMode() -> bool:
    """
    Switch Samsung Galaxy USB mode to modem mode.
    Logic adapted from: https://github.com/apeppels/galaxy-at-tool
    """
    dev = usb.core.find(
        idVendor=SAMSUNG_GALAXY_ID_VENDOR,
        idProduct=SAMSUNG_GALAXY_ID_PRODUCT,
        backend=backend,
    )

    if dev is None:
        print("No Samsung device detected over USB")
        return False

    # Device detected
    print(
        f"Samsung device {dev.product} from {dev.manufacturer} detected with "
        f"{dev.bNumConfigurations} available USB configurations"
    )

    actualConfig = dev.get_active_configuration().bConfigurationValue
    print(f"Device is currently in USB configuration {actualConfig}")

    # Already in modem mode?
    if actualConfig == USB_MODEM_CONFIGURATION:
        print(
            f"Device is already in modem mode (config {USB_MODEM_CONFIGURATION}), "
            "skipping USB switching"
        )
        return True

    # Try switching configuration
    is_ok = setUSBConfig(dev, USB_MODEM_CONFIGURATION)
    if not is_ok:
        print("First attempt failed, retrying...")
        is_ok = setUSBConfig(dev, USB_MODEM_CONFIGURATION)

    if is_ok:
        print("USB configuration successfully switched to modem mode")
    else:
        print(
            f"Unable to set USB configuration {USB_MODEM_CONFIGURATION}. "
            "This can happen if USB debugging is already enabled."
        )

    return is_ok


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    samsungGalaxyToModemMode()
