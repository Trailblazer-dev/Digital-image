# Digital Image Processing with Python

This project provides a Python-based alternative to MATLAB for digital image processing tasks. It includes implementations of common image processing operations using libraries like OpenCV, scikit-image, and PIL/Pillow.

## Setup

### Requirements
- Python 3.7 or higher
- Required libraries: see requirements.txt
- Tkinter for the GUI interface (usually comes with Python)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/digital-image.git
   cd digital-image
   ```

2. Create a virtual environment (required):
   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On Linux/macOS:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Install the package in development mode:
   ```
   pip install -e .
   ```

### Installing Tkinter

Tkinter is Python's standard GUI toolkit and is needed for the GUI interface. It usually comes with Python, but in some environments (especially minimal installations), it might be missing.

To install tkinter:

- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora/RHEL**: `sudo dnf install python3-tkinter`
- **macOS with Homebrew**: `brew install python-tk`
- **Windows**: Tkinter is included in the standard Python installer

## Project Structure

- `digital_image/`: Main package containing the implementation
  - `basic_operations.py`: Basic image operations (loading, saving, display)
  - `filters.py`: Various image filtering techniques
  - `transformations.py`: Image transformations (Fourier, perspective, etc.)
  - `segmentation.py`: Image segmentation techniques
- `examples/`: Example scripts demonstrating the functionality
- `tests/`: Unit tests for the package

## Usage

Check the examples directory for sample scripts. Basic usage:

```python
from digital_image.basic_operations import load_image, display_image
from digital_image.filters import apply_gaussian_blur

# Load an image
img = load_image('path_to_image.jpg')

# Apply gaussian blur
blurred_img = apply_gaussian_blur(img, (5, 5))

# Display the result
display_image(blurred_img, 'Blurred Image')
```

## Using the GUI Interface

The project includes a graphical user interface for interactive image processing:

## Available Functions

### Basic Operations
- Load, save, and display images
- Convert to grayscale
- Resize and rotate images

### Filters
- Gaussian blur
- Median blur
- Bilateral filter
- Edge detection (Sobel, Laplacian, Canny)
- Custom kernel application

### Transformations
- Fourier transform
- Histogram equalization
- Perspective and affine transformations

### Segmentation
- Thresholding (basic, adaptive, Otsu)
- K-means segmentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Digital-image
