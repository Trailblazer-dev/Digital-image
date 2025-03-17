#!/bin/bash

# This script activates the virtual environment and installs required packages

# Activate the virtual environment
source venv/bin/activate

# Check if activation was successful
if [ $? -eq 0 ]; then
    echo "Virtual environment activated successfully!"
    
    # Install required packages
    echo "Installing required packages..."
    pip install -r requirements.txt
    
    # Install package in development mode
    echo "Installing package in development mode..."
    pip install -e .
    
    echo ""
    echo "Setup completed successfully! You can now run the example scripts."
    echo "For example: python examples/basic_example.py"
else
    echo "Failed to activate virtual environment. Make sure it exists."
    echo "If not, create it with: python3 -m venv venv"
fi
