
import subprocess
import webbrowser
import ctypes
from ctypes import wintypes
import psutil


# Approved Windows applications
APP_COMMANDS = {
    "notepad": {
        "command": ["notepad.exe"],
        "processes": ["notepad.exe"],
    },
    "calculator": {
        "command": ["calc.exe"],
        "processes": ["calculator.exe", "calculatorapp.exe"],
    },
    "paint": {
        "command": ["mspaint.exe"],
        "processes": ["mspaint.exe"],
    },
}


# Windows API configuration
user32 = ctypes.WinDLL("user32", use_last_error=True)

EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [
    ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HWND,
        wintypes.LPARAM
    ),
    wintypes.LPARAM,
]
EnumWindows.restype = wintypes.BOOL

GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextW = user32.GetWindowTextW
IsWindowVisible = user32.IsWindowVisible
ShowWindow = user32.ShowWindow
SetForegroundWindow = user32.SetForegroundWindow
PostMessageW = user32.PostMessageW

SW_MINIMIZE = 6
SW_MAXIMIZE = 3
SW_RESTORE = 9
WM_CLOSE = 0x0010


def get_application_windows(name):
    """Find visible windows belonging to an approved application."""

    name = name.strip().lower()

    if name not in APP_COMMANDS:
        return []

    allowed_processes = APP_COMMANDS[name]["processes"]
    matching_pids = set()

    for process in psutil.process_iter(["pid", "name"]):
        try:
            process_name = (process.info["name"] or "").lower()

            if process_name in allowed_processes:
                matching_pids.add(process.info["pid"])

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    windows = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def callback(hwnd, lparam):
        if not IsWindowVisible(hwnd):
            return True

        pid = wintypes.DWORD()
        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        if pid.value not in matching_pids:
            return True

        length = GetWindowTextLengthW(hwnd)

        if length > 0:
            title = ctypes.create_unicode_buffer(length + 1)
            GetWindowTextW(hwnd, title, length + 1)
            windows.append((hwnd, title.value))

        return True

    EnumWindows(callback, 0)

    return windows


def open_application(name):
    """Open an approved Windows application."""

    name = name.strip().lower()

    if name not in APP_COMMANDS:
        return f"{name} is not in the approved application list."

    try:
        subprocess.Popen(APP_COMMANDS[name]["command"])
        return f"Opening {name}."

    except OSError as error:
        return f"Could not open {name}: {error}"


def close_application(name):
    """Request an application to close gracefully."""

    windows = get_application_windows(name)

    if not windows:
        return f"No open window found for {name}."

    for hwnd, title in windows:
        PostMessageW(hwnd, WM_CLOSE, 0, 0)

    return f"Sent a close request to {name}."


def minimize_application(name):
    """Minimize an application window."""

    windows = get_application_windows(name)

    if not windows:
        return f"No open window found for {name}."

    for hwnd, title in windows:
        ShowWindow(hwnd, SW_MINIMIZE)

    return f"Minimized {name}."


def maximize_application(name):
    """Maximize an application window."""

    windows = get_application_windows(name)

    if not windows:
        return f"No open window found for {name}."

    for hwnd, title in windows:
        ShowWindow(hwnd, SW_MAXIMIZE)

    return f"Maximized {name}."


def switch_application(name):
    """Bring an application window to the foreground."""

    windows = get_application_windows(name)

    if not windows:
        return f"No open window found for {name}."

    hwnd, title = windows[0]

    ShowWindow(hwnd, SW_RESTORE)
    SetForegroundWindow(hwnd)

    return f"Switched to {name}."


def open_website(address):
    """Open an approved website."""

    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com",
    }

    address = address.strip().lower()

    if address not in websites:
        return "That website is not in the approved list."

    webbrowser.open_new_tab(websites[address])

    return f"Opening {address}."
