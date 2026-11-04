
from automation.file_manager import (
    initialize_workspace,
    create_folder,
    create_file,
    list_files
)

print(initialize_workspace())

print("\n--- Creating folder ---")
print(create_folder("Projects"))

print("\n--- Creating file ---")
print(create_file(
    "Projects/hello.txt",
    "Hello! JARVIS file automation is working."
))

print("\n--- Listing workspace ---")
print(list_files())

print("\n--- Listing Projects ---")
print(list_files("Projects"))
