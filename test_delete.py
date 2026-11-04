
from automation.file_manager import (
    delete_file,
    delete_folder,
    create_file,
    create_folder
)

print("--- CREATE TEST FILE ---")
print(create_file("delete_test.txt", "Temporary file"))

print("\n--- DELETE FILE ---")
print(delete_file("delete_test.txt"))

print("\n--- CREATE TEST FOLDER ---")
print(create_folder("EmptyFolder"))

print("\n--- DELETE EMPTY FOLDER ---")
print(delete_folder("EmptyFolder"))
