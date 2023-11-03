#!/bin/bash

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed. Please install pip first."
    exit 1
fi

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Python dependencies installed successfully."
else
    echo "Error: Failed to install Python dependencies."
    exit 1
fi
