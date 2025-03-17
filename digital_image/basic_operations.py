import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


def load_image(file_path):
    """Load an image from a file path."""
    return cv2.imread(file_path)


def display_image(image, title='Image', cmap=None, is_bgr=True, save_path=None):
    """
    Display an image using matplotlib.
    If save_path is provided, will save the image to that path.
    """
    if is_bgr:
        # Convert BGR to RGB for matplotlib display
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(image, cmap=cmap)
    plt.title(title)
    plt.axis('off')
    
    # Save the image if a path is provided
    if save_path:
        plt.savefig(save_path)
        print(f"Image saved to: {save_path}")
    
    # Try to display, but don't fail if in a non-interactive environment
    try:
        plt.show()
    except Exception as e:
        print(f"Note: Could not display image interactively ({str(e)})")
    
    plt.close()  # Close the figure to free memory


def save_image(image, file_path, is_bgr=True):
    """Save an image to a file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    if is_bgr:
        cv2.imwrite(file_path, image)
    else:
        # Convert RGB to BGR for OpenCV saving
        cv2_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(file_path, cv2_image)
    
    print(f"Image saved to: {file_path}")


def convert_to_grayscale(image):
    """Convert an image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def resize_image(image, width=None, height=None, scale=None):
    """Resize an image based on width, height, or scale."""
    if scale:
        return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    elif width and height:
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    else:
        raise ValueError("Either scale or both width and height must be provided")


def rotate_image(image, angle, center=None, scale=1.0):
    """Rotate an image by a given angle in degrees."""
    (h, w) = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(image, M, (w, h))
