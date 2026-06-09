#!/usr/bin/env zsh

script_dir=${0:A:h}
py_path="$script_dir/auto-sorter-work.py"

if [[ -f "$py_path" ]]; then
    python3 "$py_path"
else
    echo "Error: auto-sorter-work.py not found at:"
    echo "$py_path"
    exit 1
fi