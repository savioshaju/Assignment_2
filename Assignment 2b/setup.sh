#!/bin/bash
set -e

# Detect Python version
PYTHON_BIN="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_BIN="python"
fi

PY_VER=$($PYTHON_BIN -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Detected Python version: $PY_VER"

# Create venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv venv
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found!"
    exit 1
fi

echo "Setup completed successfully!"
