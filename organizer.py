from pathlib import Path
import sys
import logging
from typing import Optional


FOLDER_PATH = (
    Path(sys.argv[0]).resolve().parent if getattr(sys, "frozen", False) else Path.cwd())  # get the path from the directory where the exe is being executed, used if the script is an executable.


extension_to_file_format = {
    # Images
    ".jpg": "Image",
    ".jpeg": "Image",
    ".png": "Image",
    ".gif": "Image",
    ".bmp": "Image",
    ".ico": "Image",
    ".svg": "Image",
    ".tiff": "Image",
    ".tif": "Image",
    ".heic": "Image",
    ".webp": "Image",
    ".psd": "Image",  # Adobe Photoshop Document
    ".ai": "Image",  # Adobe Illustrator File

    # Documents
    ".doc": "Document",
    ".docx": "Document",
    ".ppt": "Document",
    ".pptx": "Document",
    ".xls": "Document",
    ".xlsx": "Document",
    ".pdf": "Document",
    ".odt": "Document",
    ".ods": "Document",
    ".odp": "Document",
    ".txt": "Text",
    ".rtf": "Text",
    ".md": "Text",

    # Data
    ".csv": "Data",
    ".json": "Data",
    ".yaml": "Data",
    ".yml": "Data",
    ".xml": "Data",
    ".sql": "Data",

    # Databases
    ".db": "Database",
    ".sqlite": "Database",
    ".sqlite3": "Database",
    ".accdb": "Database",
    ".mdb": "Database",
    ".dbf": "Database",  # Database file, e.g., dBase, FoxPro

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".m4a": "Audio",
    ".aac": "Audio",
    ".ogg": "Audio",
    ".opus": "Audio",

    # Video
    ".mp4": "Video",
    ".m4v": "Video",
    ".mov": "Video",
    ".wmv": "Video",
    ".flv": "Video",
    ".avi": "Video",
    ".mkv": "Video",
    ".webm": "Video",

    # Ebooks
    ".epub": "Ebook",
    ".mobi": "Ebook",
    ".azw3": "Ebook",

    # Archives
    ".zip": "Archive",
    ".rar": "Archive",
    ".7z": "Archive",
    ".gz": "Archive",
    ".tar": "Archive",
    ".bz2": "Archive",
    ".xz": "Archive",
    ".zipx": "Archive",

    # Scripts
    ".sh": "Script",
    ".bat": "Script",
    ".ps1": "Script",  # PowerShell script
    ".py": "Script",
    ".rb": "Script",
    ".pl": "Script",

    # Fonts
    ".ttf": "Font",  # TrueType Font
    ".otf": "Font",  # OpenType Font
    ".woff": "Font",  # Web Open Font Format
    ".woff2": "Font",  # Web Open Font Format 2

    # 3D Models
    ".obj": "3D Model",
    ".fbx": "3D Model",
    ".dae": "3D Model",  # Collada
    ".stl": "3D Model",  # Stereolithography

    # Scientific Data
    ".nc": "Scientific Data",  # NetCDF
    ".fits": "Scientific Data",  # Flexible Image Transport System
    ".pdb": "Scientific Data",  # Protein Data Bank

    # Web files
    ".html": "Web File",
    ".css": "Web File",
    ".js": "Web File",  # JavaScript
    ".php": "Web File",
    ".asp": "Web File",
    ".aspx": "Web File",
    ".jsp": "Web File",

    # Other categories can be added.
}


def logger() -> None:
    logging.basicConfig(
        filename="Organized_files.log",
        level=logging.INFO,
        filemode="w",
        format="%(asctime)s %(message)s",
    )


logger()


def get_file_type(extension: str) -> Optional[str]:
    extension = extension.lower()
    return extension_to_file_format.get(extension, None)


def move_file_to_type_folder(file_path: Path, file_type: Optional[str]) -> None:
    if file_type:
        file_type_folder = FOLDER_PATH/file_type
        # create the type folder if it does not exist
        file_type_folder.mkdir(parents=True, exist_ok=True)
        file_destination = file_type_folder / \
            file_path.name  # final path for all the folders
        if not file_destination.exists():
            file_path.replace(file_destination)  # move the file
            logging.info(f"Moved {file_path.name} to {file_type_folder}")
        else:

            logging.info(
                f"the file {file_path.name[:20]}... already exists, skipping")
    else:
        logging.info(f"No type found for {file_path.name}, skipping. ")


def move_categorize_file(folder_path: Path) -> None:

    for file_path in folder_path.rglob("*"):
        try:
            if file_path.is_file():  # ensuring it's a file not a dir
                # get the extension of the file
                file_type = get_file_type(file_path.suffix)
                move_file_to_type_folder(file_path, file_type)

        except (FileNotFoundError, PermissionError, IsADirectoryError, FileExistsError, OSError) as e:
            print(f"An error occurred: {e}")
            logging.info(
                f"Failed to move file: {file_path.name} due to the error: {e}")


def main():
    move_categorize_file(FOLDER_PATH)


if __name__ == "__main__":
    main()
