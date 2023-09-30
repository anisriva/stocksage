#!/bin/bash

# Check if python3.9 is installed
command -v python3.9 >/dev/null 2>&1 || { echo >&2 "python3.9 is not installed. Please install python3.9 and try again."; exit 1; }

# Check if 'env' directory exists
if [ ! -d "env" ]; then
    echo "Virtual environment not found. Creating one using Python 3.9..."
    python3.9 -m venv env
    
    # Activate the virtual environment to install requirements
    source env/bin/activate

    # Install packages from requirements.txt
    if [ -f "requirements.txt" ]; then
        echo "Installing packages from requirements.txt..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Skipping package installation."
    fi
else
    # Activate the virtual environment
    source env/bin/activate
fi

# Set OPENSSL_CONF environment variable
export OPENSSL_CONF=configs/openssl.cnf

# Run main.py
python main.py
