import shutil 
import argparse
from pathlib import Path
import logging

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

#--logging------------------
LOG_FILE = Path.home() / "file_sorter.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


#--core---------------------
def extension(path: Path , dryrun: bool):
    target_dir=path
    file_found=False
    mode = "DRY-RUN" if dryrun else "LIVE"
    log.info(f"=== File Sorter [{mode}] started — watching: {target_dir} ===")
    
    for file in target_dir.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            file_found=True
            category=EXTENSION_MAP.get(file.suffix, 'Others')
            if dryrun:
                log.info(f"[DRY-RUN] Would move: {file.name} → {category}/")
                continue
            move_files (file, category, target_dir)
            
    if not file_found:
        log.info('No files to move in the target directory')
            
def move_files(file, category, target_dir):
    folder_path=Path(target_dir / category) #/images
    folder_path.mkdir(exist_ok=True)
    
    dest=folder_path / file.name #/images/open
    i=2
    
    while dest.exists():
        new_name = f'{file.stem}_{i}{file.suffix}'
        dest = folder_path / new_name #/images/open_2
        i+=1
    
    try:
        shutil.move(str(file), str(dest))
        log.info(f"Moved: {file.name} → {category}/{dest.name}")
    except Exception as e:
        log.error(f"Failed to move {file.name}: {e}")


#--cli----------------------
def cli_arguments():
    default_path=Path.home() / 'Downloads'
    parser=argparse.ArgumentParser(description='File auto sorter for the provided directory path')
    parser.add_argument('--path' , default=default_path , type=Path , help='Input file path')
    parser.add_argument('--dryrun', action='store_true', help='Preview without moving files')
    return parser.parse_args()  


def main():
    args=cli_arguments()
    extension(args.path, args.dryrun)
    
if __name__ == '__main__':
    main()