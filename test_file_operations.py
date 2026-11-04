
from automation.file_manager import (
    read_file,
    append_file,
    write_file
)

print("--- READ FILE ---")
print(read_file("Projects/hello.txt"))

print("\n--- APPEND FILE ---")
print(append_file(
    "Projects/hello.txt",
    "\nThis is the second line added by JARVIS."
))

print("\n--- READ UPDATED FILE ---")
print(read_file("Projects/hello.txt"))

print("\n--- WRITE FILE ---")
print(write_file(
    "Projects/hello.txt",
    "JARVIS file automation is working successfully."
))

print("\n--- FINAL CONTENT ---")
print(read_file("Projects/hello.txt"))
