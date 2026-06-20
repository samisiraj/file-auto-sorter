# File Extension Auto-Sorter

Automatically organizes files in a directory by type, running on a schedule via cron. Built with Python and Zsh.

## Project Structure

```
auto-sorter/
├── auto-sorter-work.py   # Core logic — scans and moves files
├── setup_sorter.sh       # Zsh script — cron management and CLI entry point
└── README.md
```

## Quick Start

```zsh
# Make the setup script executable
chmod +x setup_sorter.sh

# Preview what would happen — no files are moved
./setup_sorter.sh --dry-run

# Run once immediately
./setup_sorter.sh --run-now

# Install as an hourly cron job (default: ~/Downloads)
./setup_sorter.sh
```

## How It Works

The Zsh script is the user-facing entry point. It handles cron installation, Python path resolution, and directory validation. The Python script handles all file operations.

When run, the sorter scans the target directory (non-recursively) and moves each file into a category subfolder:

```
~/Downloads/
├── Images/
│   └── photo.png
├── Documents/
│   └── report.pdf
├── Code/
│   └── script.py
├── Archives/
│   └── backup.zip
└── Others/
    └── unknown.xyz
```

Duplicate filenames are handled automatically — if `photo.png` already exists in `Images/`, the incoming file is saved as `photo_2.png`, then `photo_3.png`, and so on. The original file in the destination is never touched.

## What Happens With No Flags

Running the script with no arguments:

```zsh
./setup_sorter.sh
```

- Targets `~/Downloads` by default
- Installs a cron job that runs the sorter every hour
- If a cron job is already installed, it is replaced (not duplicated)
- Prints the watch directory, Python path, and script location as confirmation

Running with a custom directory:

```zsh
./setup_sorter.sh ~/Desktop
```

- Same behaviour, but the cron job targets `~/Desktop` instead

## Where the Cron Job Lives

Cron jobs are stored per-user on macOS. You can view yours at any time with:

```zsh
crontab -l
```

The installed entry looks like:

```
0 * * * * /usr/bin/python3 /path/to/auto-sorter-work.py --path /Users/you/Downloads # auto-file-sorter
```

This runs at the top of every hour. The `# auto-file-sorter` tag is how the script identifies and manages its own cron entry without touching anything else in your crontab.

## If a Cron Job Already Exists

Running `./setup_sorter.sh` when a job is already installed will remove the old entry and install a fresh one with the current path. You will never end up with duplicate entries.

To check whether a job is currently installed:

```zsh
./setup_sorter.sh --status
```

## CLI Reference

| Command | What it does |
|---|---|
| `./setup_sorter.sh` | Install hourly cron job for `~/Downloads` |
| `./setup_sorter.sh ~/Desktop` | Install hourly cron job for a custom directory |
| `./setup_sorter.sh --run-now` | Sort `~/Downloads` immediately, once |
| `./setup_sorter.sh --run-now ~/Desktop` | Sort a custom directory immediately, once |
| `./setup_sorter.sh --dry-run` | Preview what would move, without moving anything |
| `./setup_sorter.sh --dry-run ~/Desktop` | Dry-run on a custom directory |
| `./setup_sorter.sh --status` | Show current cron entry |
| `./setup_sorter.sh --remove` | Remove the cron job |
| `./setup_sorter.sh --help` | Show usage |

## Extension Categories

| Category | Extensions |
|---|---|
| Images | jpg, jpeg, png, gif, bmp, svg, webp, ico, tiff |
| Videos | mp4, mkv, avi, mov, wmv, flv, webm |
| Audio | mp3, wav, flac, aac, ogg, m4a |
| Documents | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, rtf, odt, csv, md |
| Code | py, js, ts, html, css, cpp, c, java, sh, rs, go, rb, php, swift, kt |
| Archives | zip, tar, gz, rar, 7z, bz2 |
| Fonts | ttf, otf, woff, woff2 |
| Data | json, xml, yaml, yml, toml, sql, db |
| Others | anything not in the list above |

To add your own categories, open `auto-sorter-work.py` and edit `EXTENSION_MAP`:

```python
EXTENSION_MAP = {
    ".psd": "Design",
    ".epub": "Books",
    ...
}
```

## Logs

All activity is written to `~/file_sorter.log`:

```
2026-06-17 15:19:45  INFO      === File Sorter [LIVE] started — watching: /Users/you/Downloads ===
2026-06-17 15:19:45  INFO      Moved: photo.png → Images/photo.png
2026-06-17 15:19:45  INFO      Moved: report.pdf → Documents/report.pdf
```

Dry-run output looks like:

```
2026-06-17 15:19:40  INFO      === File Sorter [DRY-RUN] started — watching: /Users/you/Downloads ===
2026-06-17 15:19:40  INFO      [DRY-RUN] Would move: photo.png → Images/
```
