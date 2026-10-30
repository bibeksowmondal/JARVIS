
import subprocess
import webbrowser


# Only applications explicitly listed here can be launched.
APP_COMMANDS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
}


def open_application(name):
    """Launch an approved Windows application."""
    name = name.strip().lower()

    if name not in APP_COMMANDS:
        return (
            f"I cannot open {name}. "
            "That application is not in my approved list."
        )

    try:
        subprocess.Popen(APP_COMMANDS[name])
        return f"Opening {name}."
    except OSError as error:
        return f"Could not open {name}: {error}"


def open_website(address):
    """Open one of the explicitly approved websites."""
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com",
    }

    address = address.strip().lower()

    if address not in websites:
        return "That website is not in my approved list."

    webbrowser.open_new_tab(websites[address])
    return f"Opening {address}."
