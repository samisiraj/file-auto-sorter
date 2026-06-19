#!/usr/bin/env zsh

# --paths-----------------------------------------------------
script_dir=${0:A:h}
py_path="$script_dir/auto-sorter-work.py"
python_bin=$(command -v python3)

if [[ ! -f "$py_path" ]]; then
    echo "Error: auto-sorter-work.py not found"
    exit 1
fi

if [[ -z "$python_bin" ]]; then
    echo "Error: python3 not found"
    exit 1
fi

# --cron------------------------------------------------------
CRON_TAG="# auto-file-sorter"

install_cron() {

    watch_dir="${1:-$HOME/Downloads}"

    cron_job="0 * * * * \"$python_bin\" \"$py_path\" --path \"$watch_dir\" $CRON_TAG"

    # Don't duplicate existing cron jobs
    if crontab -l 2>/dev/null | grep -Fq "$cron_job"; then
        echo "Cron job already installed."
        return
    fi

    (
        crontab -l 2>/dev/null | grep -v "$CRON_TAG"
        echo "$cron_job"
    ) | crontab -

    echo "Cron job installed."
}

remove_cron() {
    crontab -l 2>/dev/null | grep -v "$CRON_TAG" | crontab -
    echo "Cron job removed."
}

show_status() {
    echo "Current sorter cron jobs:"
    crontab -l 2>/dev/null | grep "$CRON_TAG" || echo "No cron job installed."
}

# --actions---------------------------------------------------
case "${1:-}" in

    --remove)
        remove_cron
        ;;

    --status)
        show_status
        ;;

    --run-now)
        if [[ -n "${2:-}" ]]; then
            "$python_bin" "$py_path" --path "$2"
        else
            "$python_bin" "$py_path"
        fi
        ;;

    --dry-run)
        if [[ -n "${2:-}" ]]; then
            "$python_bin" "$py_path" --path "$2" --dryrun
        else
            "$python_bin" "$py_path" --dryrun
        fi
        ;;

    --help|-h)
        echo ""
        echo "File Sorter Setup"
        echo ""
        echo "Usage:"
        echo "  ./setup_sorter.sh [directory]"
        echo "  ./setup_sorter.sh --run-now [directory]"
        echo "  ./setup_sorter.sh --dry-run [directory]"
        echo "  ./setup_sorter.sh --status"
        echo "  ./setup_sorter.sh --remove"
        echo ""
        ;;

    *)
        watch_dir="${1:-$HOME/Downloads}"

        if [[ ! -d "$watch_dir" ]]; then
            echo "Directory does not exist:"
            echo "$watch_dir"
            exit 1
        fi

        install_cron "$watch_dir"

        echo ""
        echo "Watch directory : $watch_dir"
        echo "Python          : $python_bin"
        echo "Script          : $py_path"
        echo ""
        echo "Run now:"
        echo "  ./setup_sorter.sh --run-now \"$watch_dir\""
        echo ""
        echo "Preview:"
        echo "  ./setup_sorter.sh --dry-run \"$watch_dir\""
        ;;
esac