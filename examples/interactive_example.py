import os
import sys
import matplotlib
from pathlib import Path

# Try to use TkAgg backend for interactive plotting (must be done before importing pyplot)
try:
    matplotlib.use('TkAgg')
except ImportError:
    print("Could not set TkAgg backend, falling back to default")

# Add the parent directory to sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from digital_image.basic_operations import load_image, convert_to_grayscale
from digital_image.filters import apply_gaussian_blur, apply_canny_edge_detector
import matplotlib.pyplot as plt

# Define the sample images directory
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_images")

def main():
    # Check if matplotlib is using an interactive backend
    backend = matplotlib.get_backend()
    print(f"Current matplotlib backend: {backend}")
    is_interactive = not (backend.lower().endswith('agg') and backend.lower() != 'tkagg')
    
    if not is_interactive:
        print("Warning: Using a non-interactive backend. "
              "Images will be saved but not displayed.")
    
    # Find a sample image
    sample_path = None
    if os.path.exists(SAMPLE_DIR):
        for ext in ['.png', '.jpg', '.jpeg', '.tif', '.bmp']:
            files = list(Path(SAMPLE_DIR).glob(f'*{ext}'))
            if files:
                sample_path = str(files[0])
                break
    
    if not sample_path:
        print("No sample image found. Please run download_samples.py first.")
        return
    
    print(f"Using sample image: {sample_path}")
    
    # Load image
    img = load_image(sample_path)
    if img is None:
        print(f"Error: Could not load image at {sample_path}")
        return
    
    # Convert BGR to RGB for display
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Create a simple figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Original image
    axes[0, 0].imshow(rgb_img)
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')
    
    # Grayscale
    gray = convert_to_grayscale(img)
    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title('Grayscale')
    axes[0, 1].axis('off')
    
    # Blurred
    blurred = apply_gaussian_blur(img, (5, 5))
    axes[1, 0].imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('Gaussian Blur')
    axes[1, 0].axis('off')
    
    # Edges
    edges = apply_canny_edge_detector(img)
    axes[1, 1].imshow(edges, cmap='gray')
    axes[1, 1].set_title('Canny Edges')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    
    # Save the figure
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_images', 'image_grid.png')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)
    print(f"Saved figure to {output_file}")
    
    # Try to show the plot interactively
    try:
        plt.show()
    except Exception as e:
        print(f"Could not display plot: {e}")

if __name__ == "__main__":
    try:
        import cv2
        main()
    except ImportError:
        print("OpenCV (cv2) is required for this example. Please install it using:")
        print("pip install opencv-python")
