import shutil 
import argparse
from pathlib import Path

EXTENSION_MAP = {
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images",
    ".webp": "Images", ".ico": "Images", ".tiff": "Images",
    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos",
    ".mov": "Videos", ".wmv": "Videos", ".flv": "Videos",
    ".webm": "Videos",
    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio",
    ".aac": "Audio", ".ogg": "Audio", ".m4a": "Audio",
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".xls": "Documents", ".xlsx": "Documents", ".ppt": "Documents",
    ".pptx": "Documents", ".txt": "Documents", ".rtf": "Documents",
    ".odt": "Documents", ".csv": "Documents", ".md": "Documents",
    # Code
    ".py": "Code", ".js": "Code", ".ts": "Code", ".html": "Code",
    ".css": "Code", ".cpp": "Code", ".c": "Code", ".java": "Code",
    ".sh": "Code", ".rs": "Code", ".go": "Code", ".rb": "Code",
    ".php": "Code", ".swift": "Code", ".kt": "Code",
    # Archives
    ".zip": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".rar": "Archives", ".7z": "Archives", ".bz2": "Archives",
    # Fonts
    ".ttf": "Fonts", ".otf": "Fonts", ".woff": "Fonts", ".woff2": "Fonts",
    # Data
    ".json": "Data", ".xml": "Data", ".yaml": "Data", ".yml": "Data",
    ".toml": "Data", ".sql": "Data", ".db": "Data",
}


#core---------------------
def extension(path: Path):
    target_dir=path
    for file in target_dir.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            category=EXTENSION_MAP.get(file.suffix, 'Others')
            print(f'{file.stem} -> {category}')
            move_files (file.name, category, target_dir)
            
def move_files(file_name, category, target_dir):
    file_path= Path(target_dir / file_name)
    folder_path=Path(target_dir / category)
    folder_path.mkdir(exist_ok=True)
    shutil.move(str(file_path) , str(folder_path / file_name))


#cli----------------------
def cli_arguments():
    default_path=Path.home() / 'Downloads'
    parser=argparse.ArgumentParser(description='File auto sorter for the provided directory path')
    parser.add_argument('--path' , default=default_path , type=Path , help='Input file path')
    return parser.parse_args()  


def main():
    args=cli_arguments()
    extension(args.path)
    
if __name__ == '__main__':
    main()