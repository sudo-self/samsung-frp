"""
enable_adb.py

Enables ADB USB debugging on Samsung devices via AT commands over a serial connection.
Typically used in conjunction with usbswitcher.py to unlock USB debugging
without navigating the Android UI.
"""

import time
from typing import Optional, Union

import serial
import serial.tools.list_ports as port_list
from serial.tools import list_ports_common

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SERIAL_BAUDRATE: int = 115200
SERIAL_TIMEOUT: int = 12

# AT commands used to enable USB debugging
_ADB_COMMANDS: list[str] = [
    "AT+DUMPCTRL=1,0\r\n",
    "AT+DEBUGLVC=0,5\r\n",
    "AT+SWATD=0\r\n",
    "AT+ACTIVATE=0,0,0\r\n",
    "AT+SWATD=1\r\n",
    "AT+DEBUGLVC=0,5\r\n",
]


# ---------------------------------------------------------------------------
# Serial helpers
# ---------------------------------------------------------------------------


def list_serial_ports() -> Optional[list_ports_common.ListPortInfo]:
    """Return the first available serial port, or *None* if none are found."""
    ports = port_list.comports()
    if not ports:
        print("No serial ports available.")
        return None

    print("─" * 40)
    print("Available serial ports:")
    for port in ports:
        print(f"  {port}")
    print("─" * 40)

    return ports[0]


def open_serial(port: str) -> serial.Serial:
    """Open and return a serial connection configured for AT commands."""
    return serial.Serial(port, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT)


def send_at_command(conn: serial.Serial, cmd: str) -> Union[bool, bytes]:
    """
    Write *cmd* to *conn* and interpret the response.

    Returns:
        ``True``  – device acknowledged with ``OK``
        ``False`` – device returned ``ERROR``, an empty line, or port is closed
        ``bytes`` – raw response when the outcome is ambiguous
    """
    if not conn.isOpen():
        return False

    encoded = cmd.encode()
    print(f"  → {encoded!r}")
    conn.write(encoded)

    time.sleep(0.5)
    response = conn.read_all()
    print(f"  ← {response!r}")

    if b"OK\r\n" in response:
        return True
    if b"ERROR\r\n" in response:
        return False
    if response in (b"\r\n", b""):
        return False
    if response == encoded:
        return True

    return response


def run_at_commands(conn: serial.Serial, cmds: list[str]) -> None:
    """Send each command in *cmds* sequentially, logging results."""
    for index, cmd in enumerate(cmds):
        print(f"\n[{index + 1}/{len(cmds)}] {cmd.strip()}")
        try:
            result = send_at_command(conn, cmd)
            # Intentional: a falsy result here means the device said "OK" or
            # gave no meaningful output – that is the expected happy path.
            status = "OK" if not result else f"response={result!r}"
            print(f"  Status: {status}")
        except Exception as exc:
            print(f"  Error sending command: {exc}")

    try:
        conn.close()
        print("\nSerial connection closed.")
    except Exception as exc:
        print(f"Warning: could not close serial connection cleanly: {exc}")


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------


def enable_adb() -> None:
    """
    Interactive workflow to enable USB debugging via AT commands.

    Steps:
    1. Detect available serial ports.
    2. Ask the user whether to proceed (debugging may already be enabled).
    3. Let the user confirm the target port.
    4. Send a probe command, prompt the user to open the dialer screen, then
       send the full sequence of ADB-enable commands.
    """
    port_info = list_serial_ports()
    if port_info is None:
        return

    print(f"\nDetected device port: {port_info.device}")
    print(
        "Note: if usbswitcher.py already recognised your device, "
        "USB debugging may already be active."
    )

    proceed = (
        input(
            "\nAttempt to enable USB debugging via AT commands? [y/N] "
        ).strip().lower()
        or "n"
    )
    if proceed != "y":
        print("Skipped. Assuming USB debugging is already enabled.")
        return

    port = (
        input(f"Serial port to use [{port_info.device}]: ").strip()
        or str(port_info.device)
    )

    conn = open_serial(port)

    # Probe – checks for *#0*# mode (may not respond on all devices)
    print("\nProbing device…")
    send_at_command(conn, "AT+KSTRINGB=0,3\r\n")

    input(
        "\nOn the device, open the phone dialler and enter  *#0*#\n"
        "Press Enter here when the screen has changed… "
    )

    print("\nSending USB debugging commands…")
    run_at_commands(conn, _ADB_COMMANDS)

    print(
        "\nDone. USB debugging should now be enabled.\n"
        "If the authorisation prompt does not appear, try unplugging and "
        "replugging the USB cable."
    )


if __name__ == "__main__":
    enable_adb()
