import time
from typing import Optional, Union

import serial
import serial.tools.list_ports as prtlst
from serial.tools import list_ports_common

SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 12


def list_serial_ports() -> Optional[list_ports_common.ListPortInfo]:
    """List available serial ports and return the first one."""
    ports = prtlst.comports()
    if len(ports) == 0:
        print("No serial port available")
        return None
    print("####### Available serial ports #######")
    for port in ports:
        print(port)
    print("####### End of available serial ports #######")
    return ports[0]


def get_at_serial(port: str) -> serial.Serial:
    """Create and return a serial connection with AT command settings."""
    return serial.Serial(port, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT)


def at_send(io: serial.Serial, cmd: str) -> Union[bool, bytes]:
    """Send AT command and return the result."""
    if not io.isOpen():
        return False
    print(f"Sending {cmd.encode()}")
    io.write(cmd.encode())
    time.sleep(0.5)
    ret = io.read_all()
    print(f"Received {ret}")

    if b"OK\r\n" in ret:
        return True
    if b"ERROR\r\n" in ret:
        return False
    if ret == b"\r\n":
        return False
    if ret == cmd.encode():
        return True
    return ret != b""


def try_at_cmds(io: serial.Serial, cmds: list[str]) -> None:
    """Try multiple AT commands sequentially."""
    for i, cmd in enumerate(cmds):
        print(f"Trying method {i}")
        try:
            res = at_send(io, cmd)
            if not res:
                print("OK")
        except Exception as e:
            print(f"Error while sending command {cmd}: {e}")
    try:
        io.close()
    except Exception as e:
        print(f"Unable to properly close serial connection: {e}")


def enable_adb() -> None:
    """Enable ADB debugging via AT commands."""
    port_info = list_serial_ports()
    if not port_info:
        return

    print(f"Available serial port: {port_info.device}")
    print(
        "Since your device was detected by usbswitcher.py, "
        "USB debugging might already be enabled."
    )

    choice = (
        input(
            "Do you want to attempt enabling USB debugging via AT commands? "
            "(y/n, default=n): "
        )
        or "n"
    )

    if choice.lower() != "y":
        print("Skipping AT commands, assuming USB debugging is already enabled")
        return

    port = input(f"Choose a serial port (default={port_info.device}) :") or str(
        port_info.device
    )
    io = get_at_serial(port)
    print("Initial...")
    # Seems to check if we are in *#0*# mode but apparently not working on my device
    at_send(io, r"AT+KSTRINGB=0,3\r\n")
    print("Go to emergency dialer and enter *#0*#, press enter when done")
    input()

    print("Enabling USB Debugging...")
    cmds = []
    cmds.append(r"AT+DUMPCTRL=1,0\r\n")
    cmds.append(r"AT+DEBUGLVC=0,5\r\n")
    cmds.append(r"AT+SWATD=0\r\n")
    cmds.append(r"AT+ACTIVATE=0,0,0\r\n")
    cmds.append(r"AT+SWATD=1\r\n")
    cmds.append(r"AT+DEBUGLVC=0,5\r\n")
    try_at_cmds(io, cmds)

    print("USB Debugging should be enabled")
    print("If USB Debugging prompt does not appear, try unplug/replug the USB cable")


if __name__ == "__main__":
    enable_adb()
