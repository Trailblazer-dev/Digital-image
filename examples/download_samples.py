import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Define the sample images directory
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_images")

# Sample image URLs
SAMPLE_IMAGES = [
    {
        "name": "lenna.png", 
        "url": "https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png"
    },
    {
        "name": "cameraman.tif",
        "url": "https://homepages.inf.ed.ac.uk/rbf/HIPR2/images/cameraman.gif"
    },
    {
        "name": "baboon.png",
        "url": "https://homepages.inf.ed.ac.uk/rbf/HIPR2/images/baboon.gif"
    },
    {
        "name": "peppers.png",
        "url": "https://homepages.inf.ed.ac.uk/rbf/HIPR2/images/peppers.gif"
    }
]

def download_sample_images():
    """Download sample images for testing."""
    # Create sample images directory if it doesn't exist
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    print("Downloading sample images...")
    
    for image in SAMPLE_IMAGES:
        image_path = os.path.join(SAMPLE_DIR, image["name"])
        if not os.path.exists(image_path):
            try:
                print(f"Downloading {image['name']}...")
                urllib.request.urlretrieve(image["url"], image_path)
                print(f"Successfully downloaded {image['name']}")
            except Exception as e:
                print(f"Failed to download {image['name']}: {e}")
        else:
            print(f"{image['name']} already exists, skipping download")
    
    print(f"\nAll sample images have been downloaded to {SAMPLE_DIR}")
    print("You can now run the example scripts with these sample images.")

if __name__ == "__main__":
    download_sample_images()
