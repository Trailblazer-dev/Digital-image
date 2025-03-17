import os
import sys
import urllib.request
from pathlib import Path

# Add the parent directory to sys.path to allow importing the digital_image package
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from digital_image.basic_operations import load_image, display_image, convert_to_grayscale, save_image
from digital_image.filters import apply_gaussian_blur, apply_canny_edge_detector
from digital_image.transformations import histogram_equalization
from digital_image.segmentation import otsu_threshold

# Define the sample images directory
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_images")
# Define the output directory for processed images
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_images")

def download_sample_image():
    """Download a sample image if none exists"""
    # Create sample images directory if it doesn't exist
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    # Sample image URL (Lenna, a common test image in image processing)
    sample_url = "https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png"
    sample_path = os.path.join(SAMPLE_DIR, "lenna.png")
    
    if not os.path.exists(sample_path):
        print(f"Downloading sample image to {sample_path}...")
        try:
            urllib.request.urlretrieve(sample_url, sample_path)
            print("Sample image downloaded successfully!")
        except Exception as e:
            print(f"Failed to download sample image: {e}")
            return None
    else:
        print(f"Using existing sample image at {sample_path}")
    
    return sample_path

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Try to find a sample image in the current directory first
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for common image file extensions in the current directory
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
    found_images = []
    
    for ext in image_extensions:
        found_images.extend(list(Path(current_dir).glob(f'*{ext}')))
        if os.path.exists(SAMPLE_DIR):
            found_images.extend(list(Path(SAMPLE_DIR).glob(f'*{ext}')))
    
    if found_images:
        image_path = str(found_images[0])
        print(f"Using sample image: {image_path}")
    else:
        # No sample image found, download the default one
        print("No sample images found in the examples directory.")
        image_path = download_sample_image()
        if not image_path:
            image_path = input("Please enter the full path to an image file (or press Enter to exit): ")
            if not image_path:
                print("No image path provided. Exiting.")
                return
    
    try:
        # Load image
        img = load_image(image_path)
        if img is None:
            print(f"Error: Could not load image at {image_path}")
            return
            
        print("Image loaded successfully!")
        
        # Get base filename without extension
        base_filename = os.path.splitext(os.path.basename(image_path))[0]
        
        # Display and save original image
        orig_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_original.png")
        display_image(img, 'Original Image', save_path=orig_output_path)
        
        # Convert to grayscale
        gray_img = convert_to_grayscale(img)
        gray_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_gray.png")
        display_image(gray_img, 'Grayscale Image', cmap='gray', is_bgr=False, save_path=gray_output_path)
        
        # Apply Gaussian blur
        blurred_img = apply_gaussian_blur(img, (5, 5))
        blur_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_blurred.png")
        display_image(blurred_img, 'Blurred Image', save_path=blur_output_path)
        
        # Detect edges using Canny
        edges = apply_canny_edge_detector(img)
        edge_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_edges.png")
        display_image(edges, 'Canny Edge Detection', cmap='gray', is_bgr=False, save_path=edge_output_path)
        
        # Apply histogram equalization
        equalized_img = histogram_equalization(img)
        eq_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_equalized.png")
        display_image(equalized_img, 'Histogram Equalized', save_path=eq_output_path)
        
        # Apply Otsu thresholding
        thresholded = otsu_threshold(gray_img)
        thresh_output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_otsu.png")
        display_image(thresholded, 'Otsu Thresholding', cmap='gray', is_bgr=False, save_path=thresh_output_path)
        
        print("\nAll operations completed successfully!")
        print(f"Output images saved to: {OUTPUT_DIR}")
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
