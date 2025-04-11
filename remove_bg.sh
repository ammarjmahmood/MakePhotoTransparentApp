#!/bin/zsh

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Run the Python script with the provided image path
python3 "$SCRIPT_DIR/transparent_bg_app.py" "$1" 