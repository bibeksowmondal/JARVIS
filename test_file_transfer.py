
from automation.file_manager import (
    create_file,
    copy_file,
    move_file,
    rename_file,
    list_files
)

print("--- CREATE TEST FILE ---")
print(create_file("Projects/original.txt", "Testing file operations."))

print("\n--- COPY FILE ---")
print(copy_file(
    "Projects/original.txt",
    "Projects/copied.txt"
))

print("\n--- RENAME FILE ---")
print(rename_file(
    "Projects/copied.txt",
    "Projects/renamed.txt"
))

print("\n--- MOVE FILE ---")
print(move_file(
    "Projects/renamed.txt",
    "moved.txt"
))

print("\n--- FINAL WORKSPACE ---")
print(list_files())

print("\n--- PROJECTS FOLDER ---")
print(list_files("Projects"))

