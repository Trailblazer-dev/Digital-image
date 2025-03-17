import cv2
import numpy as np
from skimage import segmentation, color


def threshold_image(image, threshold=127, max_value=255, type=cv2.THRESH_BINARY):
    """Apply thresholding to an image."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, thresholded = cv2.threshold(image, threshold, max_value, type)
    return thresholded


def adaptive_threshold(image, max_value=255, adaptive_method=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                      threshold_type=cv2.THRESH_BINARY, block_size=11, constant=2):
    """Apply adaptive thresholding to an image."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return cv2.adaptiveThreshold(image, max_value, adaptive_method, 
                                threshold_type, block_size, constant)


def otsu_threshold(image, max_value=255, type=cv2.THRESH_BINARY):
    """Apply Otsu's thresholding to an image."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, thresholded = cv2.threshold(image, 0, max_value, type+cv2.THRESH_OTSU)
    return thresholded


def k_means_segmentation(image, k=3, attempts=10):
    """Segment an image using K-means clustering."""
    # Reshape the image to a 2D array of pixels
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    
    # Define criteria and apply K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, attempts, 
                                   cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert back to 8-bit values
    centers = np.uint8(centers)
    
    # Map the labels to the centers
    segmented_image = centers[labels.flatten()]
    
    # Reshape back to the original image dimensions
    segmented_image = segmented_image.reshape(image.shape)
    
    return segmented_image
