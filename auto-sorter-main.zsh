#!/usr/bin/env zsh

# --paths--
script_dir=${0:A:h}
py_path="$script_dir/auto-sorter-work.py"

if [[ ! -f "$py_path" ]]; then
    echo "Error: auto-sorter-work.py not found at:"
    echo "$py_path"
    exit 1
fi

if [[ -n "$1" ]]; then
    python3 "$py_path" --path "$1"
else
    python3 "$py_path"
fi