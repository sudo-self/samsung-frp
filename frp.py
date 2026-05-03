"""
sudo-self FRP Bypass Tool - PyQt5 GUI
A unified interface for USB switching, ADB debugging, FRP bypass, and SMS functions.
"""

import sys
import time
import subprocess
import threading
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QLineEdit, QTabWidget,
    QFrame, QSplitter, QScrollArea, QComboBox, QGroupBox,
    QProgressBar, QStatusBar, QSizePolicy
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation,
    QEasingCurve, QSize
)
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QTextCursor, QIcon,
    QFontDatabase, QPainter, QLinearGradient
)


# ─────────────────────────────────────────────────────────────────────────────
# Theme & Style Constants
# ─────────────────────────────────────────────────────────────────────────────

STYLE = """
QMainWindow, QWidget {
    background-color: #0b0f1a;
    color: #d4e4f7;
    font-family: 'Courier New', 'Consolas', monospace;
}

QTabWidget::pane {
    border: 1px solid #1a2540;
    background-color: #0b0f1a;
}

QTabBar::tab {
    background-color: #0d1220;
    color: #4a6a99;
    padding: 10px 24px;
    border: none;
    border-bottom: 2px solid transparent;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: bold;
}

QTabBar::tab:selected {
    color: #00d4ff;
    border-bottom: 2px solid #00d4ff;
    background-color: #111827;
}

QTabBar::tab:hover:!selected {
    color: #7aaadd;
    background-color: #0f1628;
}

QTextEdit {
    background-color: #060a12;
    color: #00d4ff;
    border: 1px solid #1a2540;
    border-radius: 4px;
    padding: 12px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    selection-background-color: #0a2a40;
}

QLineEdit {
    background-color: #0d1525;
    color: #d4e4f7;
    border: 1px solid #1e3058;
    border-radius: 3px;
    padding: 8px 12px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
}

QLineEdit:focus {
    border: 1px solid #00d4ff;
    background-color: #0f1a2e;
    color: #ffffff;
}

QLineEdit[readOnly="true"] {
    color: #d4e4f7;
}

QPushButton {
    background-color: #111827;
    color: #d4e4f7;
    border: 1px solid #1e3058;
    border-radius: 3px;
    padding: 10px 20px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    text-transform: uppercase;
}

QPushButton:hover {
    background-color: #162035;
    border: 1px solid #00d4ff;
    color: #00d4ff;
}

QPushButton:pressed {
    background-color: #090e1a;
    color: #008faa;
}

QPushButton:disabled {
    color: #2a4060;
    border-color: #141e30;
    background-color: #0d1220;
}

QPushButton#primary {
    background-color: #00131a;
    color: #00d4ff;
    border: 1px solid #00d4ff;
}

QPushButton#primary:hover {
    background-color: #001f2b;
    color: #33ddff;
    border-color: #33ddff;
}

QPushButton#danger {
    background-color: #1a0010;
    color: #ff4488;
    border: 1px solid #550033;
}

QPushButton#danger:hover {
    background-color: #260018;
    border-color: #ff4488;
}

QPushButton#success {
    background-color: #001a14;
    color: #00ffaa;
    border: 1px solid #00553a;
}

QPushButton#success:hover {
    background-color: #00261e;
    border-color: #00ffaa;
}

QComboBox {
    background-color: #0d1525;
    color: #d4e4f7;
    border: 1px solid #1e3058;
    border-radius: 3px;
    padding: 8px 12px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    min-width: 200px;
}

QComboBox:hover {
    border-color: #00d4ff;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}

QComboBox QAbstractItemView {
    background-color: #0d1525;
    color: #d4e4f7;
    border: 1px solid #1e3058;
    selection-background-color: #00131a;
    selection-color: #00d4ff;
}

QGroupBox {
    color: #4a7aaa;
    border: 1px solid #1a2d50;
    border-radius: 4px;
    margin-top: 16px;
    padding-top: 12px;
    font-family: 'Courier New', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #6a9acc;
}

QGroupBox QLineEdit {
    background-color: #0d1525;
    color: #d4e4f7;
    border: 1px solid #1e3058;
    border-radius: 3px;
    padding: 8px 12px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
}

QGroupBox QLineEdit:focus {
    border: 1px solid #00d4ff;
    background-color: #0f1a2e;
    color: #ffffff;
}

QGroupBox QLabel {
    color: #a0c4e8;
    font-family: 'Courier New', monospace;
    font-size: 12px;
}

QProgressBar {
    background-color: #0d1220;
    border: 1px solid #1a2540;
    border-radius: 2px;
    height: 4px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: #00d4ff;
    border-radius: 2px;
}

QScrollBar:vertical {
    background: #080c14;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #1e3058;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #2a4a7a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QStatusBar {
    background-color: #060a12;
    color: #4a6a99;
    border-top: 1px solid #1a2540;
    font-family: 'Courier New', monospace;
    font-size: 10px;
    letter-spacing: 1px;
}

QSplitter::handle {
    background-color: #1a2540;
    width: 1px;
}

QLabel {
    color: #a0c4e8;
    font-family: 'Courier New', monospace;
    font-size: 12px;
}

QLabel#header {
    color: #00d4ff;
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 4px;
}

QLabel#subheader {
    color: #4a6a99;
    font-size: 10px;
    letter-spacing: 3px;
}

QLabel#section {
    color: #00d4ff;
    font-size: 10px;
    letter-spacing: 3px;
    font-weight: bold;
}

QLabel#info {
    color: #7aaace;
    font-size: 11px;
}

QFrame#divider {
    background-color: #1a2540;
    max-height: 1px;
}

QFrame#card {
    background-color: #0d1220;
    border: 1px solid #1a2540;
    border-radius: 4px;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Worker Thread for non-blocking operations
# ─────────────────────────────────────────────────────────────────────────────

class Worker(QThread):
    log = pyqtSignal(str)
    done = pyqtSignal(bool)
    progress = pyqtSignal(int)

    def __init__(self, task, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.task(self.log.emit, self.progress.emit, *self.args, **self.kwargs)
            self.done.emit(True)
        except Exception as e:
            self.log.emit(f"[ERROR] {e}")
            self.done.emit(False)


# ─────────────────────────────────────────────────────────────────────────────
# Backend Logic (wrapped for GUI use)
# ─────────────────────────────────────────────────────────────────────────────

def run_adb(cmd: str, log=None) -> int:
    result = subprocess.call(f"adb {cmd}", shell=True)
    if log:
        log(f"  $ adb {cmd}  →  exit {result}")
    return result


def task_detect_usb(log, progress):
    log("checking for Samsung device...")
    try:
        import usb.backend.libusb1
        import usb.backend.libusb0
        import usb.core

        backend = usb.backend.libusb1.get_backend(
            find_library=lambda _: "/opt/homebrew/lib/libusb-1.0.dylib"
        )
        if backend is None:
            backend = usb.backend.libusb0.get_backend(
                find_library=lambda _: "/opt/homebrew/lib/libusb.dylib"
            )

        VENDOR = 0x04E8
        PRODUCT = 0x6860
        MODEM_CFG = 0x2

        dev = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT, backend=backend)
        progress(50)

        if dev is None:
            log("[WARN] No Samsung Galaxy device detected over USB.")
            return

        log(f"[OK] Device: {dev.product} by {dev.manufacturer}")
        log(f"     Configs available: {dev.bNumConfigurations}")

        active = dev.get_active_configuration().bConfigurationValue
        log(f"     Active config: {active}")

        if active == MODEM_CFG:
            log("[OK] Already in modem mode — no switch needed.")
            progress(100)
            return

        log("Switching to modem mode...")
        try:
            dev.reset()
            dev.set_configuration(MODEM_CFG)
            log("[OK] Switched to modem mode (config 2).")
        except Exception as e:
            log(f"[WARN] First attempt failed: {e}. Retrying...")
            try:
                dev.reset()
                dev.set_configuration(MODEM_CFG)
                log("[OK] Switched on second attempt.")
            except Exception as e2:
                log(f"[ERROR] Could not switch USB config: {e2}")

        progress(100)

    except ImportError:
        log("[ERROR] pyusb not installed. Run: pip install pyusb")


def task_frp_bypass(log, progress):
    log("Starting sudo-self bypass methods...")
    log("")

    commands = [
        ("settings put global setup_wizard_has_run 1",       "Mark setup wizard complete"),
        ("settings put secure user_setup_complete 1",         "Mark user setup complete"),
        ("content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1", "Provision device"),
        ("content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1", "Set user_setup_complete"),
        ("content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1", "Allow non-market apps"),
        ("am start -c android.intent.category.HOME -a android.intent.action.MAIN", "Return to home screen"),
    ]

    for i, (cmd, desc) in enumerate(commands):
        log(f"[{i+1}/{len(commands)}] {desc}")
        run_adb(f"shell {cmd}", log)
        progress(int((i + 1) / (len(commands) + 2) * 100))
        time.sleep(0.3)

    log("\nWaiting 5 seconds...")
    time.sleep(5)

    log("\nOpening Android Settings...")
    run_adb("shell am start -n com.android.settings/com.android.settings.Settings", log)
    progress(90)

    log("\n[NEXT] In Settings → go to 'Backup and reset' → Factory data reset")
    log("Rebooting device...")
    time.sleep(2)
    run_adb("shell reboot", log)
    progress(100)
    log("\n[DONE] FRP bypass complete.")


def task_push_frp_bin(log, progress):
    log("Pushing frp.bin to device...")
    run_adb("push frp.bin /data/local/tmp/temp", log)
    progress(40)
    log("Setting permissions (chmod 777)...")
    run_adb("shell chmod 777 /data/local/tmp/temp", log)
    progress(70)
    log("Executing binary...")
    run_adb("shell /data/local/tmp/temp", log)
    progress(100)
    log("[DONE] Binary executed.")


def task_wait_device(log, progress):
    log("Restarting ADB server...")
    run_adb("kill-server", log)
    progress(20)
    log("Waiting for device to connect...")
    run_adb("wait-for-device", log)
    progress(100)
    log("[OK] Device connected.")


def task_at_enable_adb(log, progress, port):
    try:
        import serial
        log(f"Opening serial port: {port}")
        import time as t

        BAUDRATE = 115200
        TIMEOUT = 12

        conn = serial.Serial(port, baudrate=BAUDRATE, timeout=TIMEOUT)
        progress(10)

        def send(cmd):
            log(f"  → {cmd.strip()!r}")
            conn.write(cmd.encode())
            t.sleep(0.5)
            resp = conn.read_all()
            log(f"  ← {resp!r}")
            return resp

        log("Probing device (AT+KSTRINGB)...")
        send("AT+KSTRINGB=0,3\r\n")
        progress(20)

        cmds = [
            ("AT+DUMPCTRL=1,0\r\n",    "Enable dump control"),
            ("AT+DEBUGLVC=0,5\r\n",    "Set debug LVC"),
            ("AT+SWATD=0\r\n",         "Disable SWATD"),
            ("AT+ACTIVATE=0,0,0\r\n",  "Activate debug mode"),
            ("AT+SWATD=1\r\n",         "Re-enable SWATD"),
            ("AT+DEBUGLVC=0,5\r\n",    "Set debug LVC again"),
        ]

        for i, (cmd, desc) in enumerate(cmds):
            log(f"\n[{i+1}/{len(cmds)}] {desc}")
            send(cmd)
            progress(20 + int((i + 1) / len(cmds) * 75))

        conn.close()
        progress(100)
        log("\n[DONE] USB debugging commands sent.")
        log("no workie? try Unplug and replug USB cable")

    except ImportError:
        log("[ERROR] pyserial not installed. Run: pip install pyserial")
    except Exception as e:
        log(f"[ERROR] {e}")


def list_serial_ports_gui():
    try:
        import serial.tools.list_ports as prtlst
        ports = prtlst.comports()
        return [str(p.device) for p in ports]
    except ImportError:
        return []


def task_receive_sms(log, progress, port):
    try:
        import serial
        import time as t

        log(f"Connecting to modem on {port}...")
        conn = serial.Serial(port, 115200, timeout=12)
        progress(10)

        def send(cmd):
            conn.write(cmd.encode())
            t.sleep(2)
            resp = conn.readline()
            log(f"  {resp}")
            return resp

        send("ATZ\r")
        send("AT+CMGF=1\r")
        conn.flushInput()
        conn.flushOutput()
        send("AT\r")
        progress(40)

        log("Checking for unread messages...")
        conn.write(b'AT+CMGL="REC UNREAD"\r')
        t.sleep(2)
        response = conn.read_all().decode(errors="replace")
        progress(80)

        if "REC UNREAD" in response:
            idx_num = response.find('+255')
            idx_sms = response.find('"\\r\\n') + 5
            idx_end = response.find('\\r\\n\\r\\nOK\\r\\n')
            phone = response[idx_num:idx_num+13]
            sms = response[idx_sms:idx_end]
            log(f"\n[SMS RECEIVED]")
            log(f"  From : {phone}")
            log(f"  Body : {sms}")
        else:
            log("[INFO] No unread messages found.")

        conn.close()
        progress(100)

    except ImportError:
        log("[ERROR] pyserial not installed.")
    except Exception as e:
        log(f"[ERROR] {e}")


def task_send_sms(log, progress, port, number, message):
    try:
        import serial
        import time as t

        log(f"Connecting to modem on {port}...")
        conn = serial.Serial(port, 115200, timeout=12)
        progress(10)

        def send(cmd, wait=True):
            conn.write(cmd.encode())
            if wait:
                t.sleep(2)
                resp = conn.readline()
                log(f"  ← {resp}")

        send("ATZ\r")
        send("ATE0\r")
        send("AT+CMGD=\"ALL\"\r")
        send("AT+CMGF=1\r")
        progress(50)

        log(f"Sending to {number}...")
        send(f'AT+CMGS="{number}"\r')
        send(message + "\r")
        conn.write(chr(26).encode())
        t.sleep(3)
        resp = conn.read_all()
        log(f"  ← {resp}")
        progress(90)

        conn.flush()
        conn.close()
        progress(100)
        log("[DONE] SMS sent.")

    except ImportError:
        log("[ERROR] pyserial not installed.")
    except Exception as e:
        log(f"[ERROR] {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Reusable UI Components
# ─────────────────────────────────────────────────────────────────────────────

class LogConsole(QTextEdit):
    """Green-on-black terminal output console."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMinimumHeight(220)

    def log(self, text: str, color: str = "#00d4ff"):
        self.moveCursor(QTextCursor.End)
        self.setTextColor(QColor(color))
        self.insertPlainText(text + "\n")
        self.moveCursor(QTextCursor.End)

    def log_warn(self, text: str):
        self.log(text, "#ffcc00")

    def log_error(self, text: str):
        self.log(text, "#ff4488")

    def clear_log(self):
        self.clear()
        self.log("─" * 56, "#1a2d50")


class StatusDot(QLabel):
    """Small colored status indicator dot."""

    def __init__(self, parent=None):
        super().__init__("●", parent)
        self.setFont(QFont("Courier New", 10))
        self.set_idle()

    def set_idle(self):
        self.setStyleSheet("color: #1e3058;")

    def set_active(self):
        self.setStyleSheet("color: #00d4ff;")

    def set_ok(self):
        self.setStyleSheet("color: #00ffaa;")

    def set_error(self):
        self.setStyleSheet("color: #ff4488;")


class SectionLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text.upper(), parent)
        self.setObjectName("section")


class InfoLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("info")
        self.setWordWrap(True)


class Divider(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("divider")
        self.setFrameShape(QFrame.HLine)
        self.setFixedHeight(1)


class ActionButton(QPushButton):
    def __init__(self, text, style="normal", parent=None):
        super().__init__(text, parent)
        if style == "primary":
            self.setObjectName("primary")
        elif style == "danger":
            self.setObjectName("danger")
        elif style == "success":
            self.setObjectName("success")
        self.setCursor(Qt.PointingHandCursor)


# ─────────────────────────────────────────────────────────────────────────────
# Tab: USB Switcher
# ─────────────────────────────────────────────────────────────────────────────

class USBTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Header
        hdr = QHBoxLayout()
        self.dot = StatusDot()
        hdr.addWidget(self.dot)
        hdr.addSpacing(8)
        hdr.addWidget(SectionLabel("USB Mode Switcher"))
        hdr.addStretch()
        layout.addLayout(hdr)

        layout.addWidget(InfoLabel(
            "Switches the Samsung Galaxy USB configuration from MFC/PTP mode to Modem mode "
            "(config 2). Required before sending AT commands. Uses libusb — device must be plugged in."
        ))

        layout.addWidget(Divider())

        # Buttons row
        btn_row = QHBoxLayout()
        self.btn_detect = ActionButton("Detect Device", "primary")
        self.btn_switch = ActionButton("Switch to Modem Mode")
        self.btn_detect.clicked.connect(self.detect)
        self.btn_switch.clicked.connect(self.detect)
        btn_row.addWidget(self.btn_detect)
        btn_row.addWidget(self.btn_switch)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Progress
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Console
        self.console = LogConsole()
        self.console.log("Ready. Plug in device and click Detect.", "#2a4a6a")
        layout.addWidget(self.console)

    def detect(self):
        self.console.clear_log()
        self.progress.setValue(0)
        self.dot.set_active()
        self.btn_detect.setEnabled(False)

        self.worker = Worker(task_detect_usb)
        self.worker.log.connect(self.console.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.done.connect(self._done)
        self.worker.start()

    def _done(self, ok):
        self.btn_detect.setEnabled(True)
        if ok:
            self.dot.set_ok()
        else:
            self.dot.set_error()


# ─────────────────────────────────────────────────────────────────────────────
# Tab: ADB / AT Commands
# ─────────────────────────────────────────────────────────────────────────────

class ADBTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        layout.addWidget(SectionLabel("ADB & AT Command Control"))
        layout.addWidget(InfoLabel(
            "Enable USB debugging via AT commands over serial, or wait for ADB device connection."
        ))
        layout.addWidget(Divider())

        # Serial port selector
        port_row = QHBoxLayout()
        port_row.addWidget(QLabel("Serial Port:"))
        self.port_combo = QComboBox()
        self.port_combo.setEditable(True)
        self.refresh_ports()
        port_row.addWidget(self.port_combo)

        self.btn_refresh = ActionButton("↻ Refresh")
        self.btn_refresh.setFixedWidth(90)
        self.btn_refresh.clicked.connect(self.refresh_ports)
        port_row.addWidget(self.btn_refresh)
        port_row.addStretch()
        layout.addLayout(port_row)

        layout.addWidget(InfoLabel(
            "Step 1: On the device, open phone dialer and enter  *#0*#  to enter service mode.\n"
            "Step 2: Click 'Send AT Commands' below."
        ))

        # Buttons
        btn_row = QHBoxLayout()
        self.btn_at = ActionButton("Send AT Commands", "primary")
        self.btn_wait = ActionButton("Wait for Device (ADB)")
        self.btn_at.clicked.connect(self.send_at)
        self.btn_wait.clicked.connect(self.wait_device)
        btn_row.addWidget(self.btn_at)
        btn_row.addWidget(self.btn_wait)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.console = LogConsole()
        self.console.log("Select a serial port and click 'Send AT Commands'.", "#2a4a6a")
        layout.addWidget(self.console)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = list_serial_ports_gui()
        if ports:
            self.port_combo.addItems(ports)
        else:
            self.port_combo.addItem("No ports found")

    def send_at(self):
        port = self.port_combo.currentText()
        if not port or port == "No ports found":
            self.console.log_warn("[WARN] No serial port selected.")
            return
        self.console.clear_log()
        self.progress.setValue(0)
        self.btn_at.setEnabled(False)

        self.worker = Worker(task_at_enable_adb, port)
        self.worker.log.connect(self.console.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.done.connect(lambda ok: self.btn_at.setEnabled(True))
        self.worker.start()

    def wait_device(self):
        self.console.clear_log()
        self.progress.setValue(0)
        self.btn_wait.setEnabled(False)

        self.worker = Worker(task_wait_device)
        self.worker.log.connect(self.console.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.done.connect(lambda ok: self.btn_wait.setEnabled(True))
        self.worker.start()


# ─────────────────────────────────────────────────────────────────────────────
# Tab: FRP Bypass
# ─────────────────────────────────────────────────────────────────────────────

class FRPTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        layout.addWidget(SectionLabel("FRP Bypass"))
        layout.addWidget(InfoLabel(
            "Factory Reset Protection bypass via ADB commands. Device must have ADB "
            "enabled and be connected. Two methods available: manual ADB commands or "
            "binary push (frp.bin must be present in current directory)."
        ))
        layout.addWidget(Divider())

        # Method A
        grp_a = QGroupBox("Method A — ADB Settings Commands")
        grp_a_layout = QVBoxLayout(grp_a)
        grp_a_layout.addWidget(InfoLabel(
            "Writes to Android settings database to mark device as provisioned, "
            "then opens Settings for factory reset."
        ))
        self.btn_manual = ActionButton("Run ADB Bypass", "primary")
        self.btn_manual.clicked.connect(self.run_manual)
        grp_a_layout.addWidget(self.btn_manual)
        layout.addWidget(grp_a)

        # Method B
        grp_b = QGroupBox("Method B — Push frp.bin Binary")
        grp_b_layout = QVBoxLayout(grp_b)
        grp_b_layout.addWidget(InfoLabel(
            "Pushes and executes frp.bin from current directory. "
            "Requires ro.secure=1 on the device."
        ))
        self.btn_bin = ActionButton("Push & Execute frp.bin", "danger")
        self.btn_bin.clicked.connect(self.run_bin)
        grp_b_layout.addWidget(self.btn_bin)
        layout.addWidget(grp_b)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.console = LogConsole()
        self.console.log("Select a method above. Device must be connected via ADB.", "#2a4a6a")
        layout.addWidget(self.console)

    def run_manual(self):
        self.console.clear_log()
        self.progress.setValue(0)
        self.btn_manual.setEnabled(False)

        self.worker = Worker(task_frp_bypass)
        self.worker.log.connect(self.console.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.done.connect(lambda ok: self.btn_manual.setEnabled(True))
        self.worker.start()

    def run_bin(self):
        self.console.clear_log()
        self.progress.setValue(0)
        self.btn_bin.setEnabled(False)

        self.worker = Worker(task_push_frp_bin)
        self.worker.log.connect(self.console.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.done.connect(lambda ok: self.btn_bin.setEnabled(True))
        self.worker.start()


# ─────────────────────────────────────────────────────────────────────────────
# Tab: SMS Tool
# ─────────────────────────────────────────────────────────────────────────────

class SMSTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(24)

        layout.addWidget(SectionLabel("GSM Modem SMS"))
        layout.addWidget(InfoLabel(
            "Send and receive SMS messages via a GSM modem connected over serial."
        ))
        layout.addWidget(Divider())

        # Port row
        port_row = QHBoxLayout()
        port_row.addWidget(QLabel("Modem Port:"))
        self.port_combo = QComboBox()
        self.port_combo.setEditable(True)
        ports = list_serial_ports_gui()
        if ports:
            self.port_combo.addItems(ports)
        else:
            self.port_combo.addItem("COM5")
        port_row.addWidget(self.port_combo)

        btn_refresh = ActionButton("↻")
        btn_refresh.setFixedWidth(40)
        btn_refresh.clicked.connect(self._refresh_ports)
        port_row.addWidget(btn_refresh)
        port_row.addStretch()
        layout.addLayout(port_row)

        layout.addWidget(Divider())

        # Receive group
        grp_rx = QGroupBox("Receive SMS")
        grp_rx_layout = QHBoxLayout(grp_rx)
        self.btn_receive = ActionButton("Check Unread Messages", "success")
        self.btn_receive.clicked.connect(self.receive)
        grp_rx_layout.addWidget(self.btn_receive)
        grp_rx_layout.addStretch()
        layout.addWidget(grp_rx)

        # Send group
        grp_tx = QGroupBox("Send SMS")
        grp_tx_layout = QVBoxLayout(grp_tx)

        num_row = QHBoxLayout()
        num_row.addWidget(QLabel("To:"))
        self.input_number = QLineEdit()
        self.input_number.setPlaceholderText("+1234567890")
        num_row.addWidget(self.input_number)
        grp_tx_layout.addLayout(num_row)

        grp_tx_layout.addWidget(QLabel("Message:"))
        self.input_msg = QLineEdit()
        self.input_msg.setPlaceholderText("add your message here...")
        grp_tx_layout.addWidget(self.input_msg)

        self.btn_send = ActionButton("Send SMS", "primary")
        self.btn_send.clicked.connect(self.send)
        grp_tx_layout.addWidget(self.btn_send)
        layout.addWidget(grp_tx)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.console = LogConsole()
        self.console.log("GSM modem SMS tool ready.", "#2a4a6a")
        layout.addWidget(self.console)

    def _refresh_ports(self):
        self.port_combo.clear()
        ports = list_serial_ports_gui()
        self.port_combo.addItems(ports or ["No ports found"])

    def receive(self):
        port = self.port_combo.currentText()
        self.console.clear_log()
        self.progress.setValue(0)
        self.btn_receive.setEnabled(False)

        self.worker = Worker(task_receive_sms, port)
        self.worker.log.connect(self.console.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.done.connect(lambda ok: self.btn_receive.setEnabled(True))
        self.worker.start()

    def send(self):
        port = self.port_combo.currentText()
        number = self.input_number.text().strip()
        message = self.input_msg.text().strip()

        if not number:
            self.console.log_warn("[WARN] Enter a phone number.")
            return
        if not message:
            self.console.log_warn("[WARN] Enter a message.")
            return

        self.console.clear_log()
        self.progress.setValue(0)
        self.btn_send.setEnabled(False)

        self.worker = Worker(task_send_sms, port, number, message)
        self.worker.log.connect(self.console.log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.done.connect(lambda ok: self.btn_send.setEnabled(True))
        self.worker.start()


# ─────────────────────────────────────────────────────────────────────────────
# Main Window
# ─────────────────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Samsung FRP Tool")
        self.setMinimumSize(820, 680)
        self.resize(900, 900)
        self._build()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header bar ──────────────────────────────────────────────────────
        header_bar = QFrame()
        header_bar.setStyleSheet("""
            QFrame {
                background-color: #060a12;
                border-bottom: 1px solid #1a2540;
            }
        """)
        header_bar.setFixedHeight(72)
        hbl = QHBoxLayout(header_bar)
        hbl.setContentsMargins(28, 0, 28, 0)

        title = QLabel("SAMSUNG FRP TOOL")
        title.setObjectName("header")
        hbl.addWidget(title)

        hbl.addStretch()

        ver = QLabel("sudo-self")
        ver.setStyleSheet("color: #2a4060; font-size: 10px; letter-spacing: 2px;")
        hbl.addWidget(ver)

        root.addWidget(header_bar)

        # ── Tabs ────────────────────────────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.addTab(USBTab(),  "USB")
        self.tabs.addTab(ADBTab(),  "ADB")
        self.tabs.addTab(FRPTab(),  "FRP")
        self.tabs.addTab(SMSTab(),  "SMS")
        root.addWidget(self.tabs)

        # ── Status bar ──────────────────────────────────────────────────────
        status = self.statusBar()
        status.showMessage("  READY  ·  Connect device via USB  ·  Python " + sys.version.split()[0])


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    app.setApplicationName("Samsung FRP Tool")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
