
import os
import shutil
from pathlib import Path


# JARVIS workspace
WORKSPACE = Path.home() / "Documents" / "JARVIS_Workspace"


def initialize_workspace():
    """Create the JARVIS workspace if it does not exist."""
    try:
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        return f"Workspace ready at {WORKSPACE}"
    except OSError as error:
        return f"Could not initialize workspace: {error}"


def get_safe_path(name):
    """Resolve a path while preventing access outside the workspace."""
    if not name or not name.strip():
        raise ValueError("Please provide a file or folder name.")

    path = (WORKSPACE / name).resolve()

    if not path.is_relative_to(WORKSPACE.resolve()):
        raise ValueError("Access outside the JARVIS workspace is not allowed.")

    return path


def create_folder(folder_name):
    """Create a folder inside the JARVIS workspace."""
    try:
        folder = get_safe_path(folder_name)
        folder.mkdir(parents=True, exist_ok=True)

        return f"Folder created: {folder.name}"

    except (OSError, ValueError) as error:
        return f"Could not create folder: {error}"


def create_file(file_name, content=""):
    """Create a text file inside the JARVIS workspace."""
    try:
        file_path = get_safe_path(file_name)

        if file_path.exists():
            return "A file with that name already exists."

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        return f"File created: {file_path.name}"

    except (OSError, ValueError) as error:
        return f"Could not create file: {error}"


def list_files(folder_name=""):
    """List files and folders inside the workspace."""
    try:
        folder = get_safe_path(folder_name) if folder_name else WORKSPACE

        if not folder.exists():
            return "The requested folder does not exist."

        if not folder.is_dir():
            return "The requested path is not a folder."

        items = sorted(
            folder.iterdir(),
            key=lambda item: (not item.is_dir(), item.name.lower())
        )

        if not items:
            return "The folder is empty."

        result = []

        for item in items:
            item_type = "Folder" if item.is_dir() else "File"
            result.append(f"{item_type}: {item.name}")

        return "\n".join(result)

    except (OSError, ValueError) as error:
        return f"Could not list files: {error}"


def read_file(file_name):
    """Read a text file inside the workspace."""
    try:
        file_path = get_safe_path(file_name)

        if not file_path.is_file():
            return "File does not exist."

        content = file_path.read_text(encoding="utf-8")
        return content if content else "The file is empty."

    except (OSError, ValueError) as error:
        return f"Could not read file: {error}"


def append_file(file_name, content):
    """Append text to an existing file."""
    try:
        file_path = get_safe_path(file_name)

        if not file_path.is_file():
            return "File does not exist."

        with file_path.open("a", encoding="utf-8") as file:
            file.write(content)

        return f"Content appended to {file_path.name}."

    except (OSError, ValueError) as error:
        return f"Could not append content: {error}"


def write_file(file_name, content):
    """Replace the contents of an existing file."""
    try:
        file_path = get_safe_path(file_name)

        if not file_path.is_file():
            return "File does not exist."

        file_path.write_text(content, encoding="utf-8")
        return f"Updated {file_path.name}."

    except (OSError, ValueError) as error:
        return f"Could not write file: {error}"


def copy_file(source_name, destination_name):
    """Copy a file inside the workspace."""
    try:
        source = get_safe_path(source_name)
        destination = get_safe_path(destination_name)

        if not source.is_file():
            return "Source file does not exist."

        if destination.exists():
            return "Destination already exists."

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        return f"Copied {source.name} successfully."

    except (OSError, ValueError) as error:
        return f"Could not copy file: {error}"


def move_file(source_name, destination_name):
    """Move a file inside the workspace."""
    try:
        source = get_safe_path(source_name)
        destination = get_safe_path(destination_name)

        if not source.is_file():
            return "Source file does not exist."

        if destination.exists():
            return "Destination already exists."

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))

        return f"Moved {source.name} successfully."

    except (OSError, ValueError) as error:
        return f"Could not move file: {error}"


def rename_file(old_name, new_name):
    """Rename a file inside the workspace."""
    try:
        old_path = get_safe_path(old_name)
        new_path = get_safe_path(new_name)

        if not old_path.is_file():
            return "File does not exist."

        if new_path.exists():
            return "A file with the new name already exists."

        old_path.rename(new_path)

        return f"Renamed file to {new_path.name}."

    except (OSError, ValueError) as error:
        return f"Could not rename file: {error}"


def delete_file(file_name):
    """Delete a file inside the workspace."""
    try:
        file_path = get_safe_path(file_name)

        if not file_path.is_file():
            return "File does not exist."

        file_path.unlink()

        return f"File deleted: {file_path.name}"

    except (OSError, ValueError) as error:
        return f"Could not delete file: {error}"


def delete_folder(folder_name):
    """Delete an empty folder inside the workspace."""
    try:
        folder_path = get_safe_path(folder_name)

        if not folder_path.is_dir():
            return "Folder does not exist."

        if folder_path == WORKSPACE.resolve():
            return "Cannot delete the main JARVIS workspace."

        folder_path.rmdir()

        return f"Empty folder deleted: {folder_path.name}"

    except OSError as error:
        return (
            "Could not delete folder. "
            "It may not be empty."
        )

    except ValueError as error:
        return f"Invalid folder: {error}"
