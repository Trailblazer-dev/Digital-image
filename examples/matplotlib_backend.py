import os
import sys
import matplotlib
from pathlib import Path

# Add the parent directory to sys.path to allow importing the digital_image package
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

def setup_matplotlib_backend():
    """
    Set up the matplotlib backend based on the environment
    Returns the current backend name
    """
    print("Available matplotlib backends:")
    print(matplotlib.rcsetup.all_backends)
    
    # Check current backend
    current_backend = matplotlib.get_backend()
    print(f"Current matplotlib backend: {current_backend}")
    
    # Try to determine the best backend for this environment
    is_interactive = hasattr(sys, 'ps1')
    in_ipython = 'ipykernel' in sys.modules
    in_notebook = 'IPython.core.interactiveshell' in sys.modules
    no_display = 'DISPLAY' not in os.environ
    
    print(f"Environment info:")
    print(f"- Interactive shell: {is_interactive}")
    print(f"- IPython: {in_ipython}")
    print(f"- Notebook: {in_notebook}")
    print(f"- No display: {no_display}")
    
    # Suggest a backend based on the environment
    if in_notebook:
        suggested_backend = 'nbAgg'
    elif no_display:
        suggested_backend = 'Agg'
    else:
        if sys.platform.startswith('linux'):
            suggested_backend = 'TkAgg'
        elif sys.platform.startswith('win'):
            suggested_backend = 'TkAgg'
        elif sys.platform.startswith('darwin'):
            suggested_backend = 'MacOSX'
        else:
            suggested_backend = 'TkAgg'
    
    print(f"Suggested backend for your environment: {suggested_backend}")
    
    # Set the backend if needed
    if suggested_backend != current_backend:
        print(f"To change the backend, add this line to your script:")
        print(f"import matplotlib\nmatplotlib.use('{suggested_backend}')\n")
        print("NOTE: This must be done before importing pyplot.")
    
    return current_backend

if __name__ == "__main__":
    setup_matplotlib_backend()
    
    print("\nExample usage in scripts:")
    print("```python")
    print("import matplotlib")
    print("matplotlib.use('Agg')  # Non-interactive backend (for saving figures)")
    print("# or")
    print("matplotlib.use('TkAgg')  # Interactive backend (for displaying figures)")
    print("import matplotlib.pyplot as plt")
    print("```")
    
    # Try to import pyplot
    try:
        import matplotlib.pyplot as plt
        print("\nSuccessfully imported matplotlib.pyplot")
    except Exception as e:
        print(f"\nFailed to import matplotlib.pyplot: {e}")
