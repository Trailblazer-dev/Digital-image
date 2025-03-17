#!/bin/bash

# This script installs system dependencies needed for the GUI interface

# Detect OS
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
else
    # Fall back to uname
    OS=$(uname -s)
    VER=$(uname -r)
fi

echo "Detected OS: $OS $VER"
echo "Installing required system packages for the GUI interface..."

# Install packages based on OS
if [[ $OS == *"Ubuntu"* ]] || [[ $OS == *"Debian"* ]]; then
    echo "Installing packages for Ubuntu/Debian..."
    sudo apt-get update
    sudo apt-get install -y python3-tk python3-pil.imagetk
elif [[ $OS == *"Fedora"* ]] || [[ $OS == *"CentOS"* ]] || [[ $OS == *"Red Hat"* ]]; then
    echo "Installing packages for Fedora/RHEL/CentOS..."
    sudo dnf install -y python3-tkinter python3-pillow-tk
elif [[ $OS == *"Arch"* ]]; then
    echo "Installing packages for Arch Linux..."
    sudo pacman -Sy python-tk python-pillow
elif [[ $OS == *"Darwin"* ]] || [[ $OS == *"macOS"* ]]; then
    echo "For macOS, we recommend using Homebrew:"
    echo "brew install python-tk"
    echo "You may need to reinstall pillow: pip uninstall Pillow && pip install --upgrade Pillow"
elif [[ $OS == *"MINGW"* ]] || [[ $OS == *"MSYS"* ]] || [[ $OS == *"Windows"* ]]; then
    echo "For Windows, tkinter should be included with Python."
    echo "Make sure you have Pillow installed: pip install --upgrade Pillow"
else
    echo "Unsupported OS: $OS"
    echo "Please install the following packages manually:"
    echo "- tkinter for Python3"
    echo "- PIL.ImageTk (usually part of python-pillow or python-pil packages)"
fi

echo "Installation complete. Try running the GUI interface now:"
echo "python examples/gui_interface.py"
