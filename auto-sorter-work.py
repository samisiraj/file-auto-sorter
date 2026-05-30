import os 
import shutil 
import argparse
from pathlib import Path

def extension(path: Path):
    target_dir=path
    for file in target_dir.iterdir():
        if file.is_file():
            print(f'file name {file.stem}, file extension {file.suffix}')

def main():
    default_path=Path.home() / 'Downloads'
    parser=argparse.ArgumentParser(description='File auto sorter for the provided directory path')
    parser.add_argument('--path' , default=default_path , type=Path , help='Input file path')
    args=parser.parse_args()
    
    extension(args.path)
    
if __name__ == '__main__':
    main()