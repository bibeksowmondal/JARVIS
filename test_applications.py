
from automation.applications import (
    open_application,
    close_application,
    minimize_application,
    maximize_application,
    switch_application,
)

print("JARVIS APPLICATION AUTOMATION TEST")

print("\n1.", open_application("notepad"))
input("Press Enter after Notepad opens...")

print("\n2.", minimize_application("notepad"))
input("Press Enter to continue...")

print("\n3.", maximize_application("notepad"))
input("Press Enter to continue...")

print("\n4.", switch_application("notepad"))
input("Press Enter to close Notepad...")

print("\n5.", close_application("notepad"))

print("\nApplication automation test completed.")
