#!/usr/bin/env python3
"""
This script detects the environment and runs the best example for the current setup.
It will try to run the GUI interface if possible, otherwise fall back to the command-line example.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def check_display():
    """Check if a display is available"""
    return 'DISPLAY' in os.environ

def main():
    """Run the best example for the current environment"""
    # Get the directory of this script
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if we can run the GUI version
    has_tkinter = check_tkinter()
    has_display = check_display()
    
    print("Environment check:")
    print(f"- Tkinter available: {'✓' if has_tkinter else '✗'}")
    print(f"- Display available: {'✓' if has_display else '✗'}")
    
    if has_tkinter and has_display:
        print("\nRunning GUI interface...")
        gui_script = script_dir / "gui_interface.py"
        
        try:
            result = subprocess.run([sys.executable, str(gui_script)], check=False)
            if result.returncode != 0:
                print("\nFailed to run GUI interface, falling back to command-line example")
                basic_script = script_dir / "basic_example.py"
                subprocess.run([sys.executable, str(basic_script)], check=False)
        except Exception as e:
            print(f"Error running GUI interface: {e}")
            print("Falling back to command-line example")
            basic_script = script_dir / "basic_example.py"
            subprocess.run([sys.executable, str(basic_script)], check=False)
    else:
        print("\nRunning command-line example (GUI requirements not met)...")
        basic_script = script_dir / "basic_example.py"
        subprocess.run([sys.executable, str(basic_script)], check=False)
        
        if not has_tkinter:
            print("\nTo use the GUI interface, you need to install tkinter:")
            print("- Ubuntu/Debian: sudo apt-get install python3-tk")
            print("- Fedora/RHEL: sudo dnf install python3-tkinter")
            print("- macOS with Homebrew: brew install python-tk")
            print("- Windows: Tkinter should be included with Python")
        
        if not has_display:
            print("\nNo display detected. If you're on a remote server, try:")
            print("- Using X11 forwarding: ssh -X user@server")
            print("- Setting up a VNC server")
            print("- Using a different example that doesn't require a display")

if __name__ == "__main__":
    main()
