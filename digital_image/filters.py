import cv2
import numpy as np
from scipy import ndimage


def apply_gaussian_blur(image, kernel_size=(5, 5), sigma=0):
    """Apply Gaussian blur to an image."""
    return cv2.GaussianBlur(image, kernel_size, sigma)


def apply_median_blur(image, kernel_size=5):
    """Apply median blur to an image."""
    return cv2.medianBlur(image, kernel_size)


def apply_bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """Apply bilateral filter to an image (edge-preserving smoothing)."""
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


def apply_sobel_filter(image, dx=1, dy=1, ksize=3):
    """Apply Sobel filter for edge detection."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return cv2.Sobel(image, cv2.CV_64F, dx, dy, ksize=ksize)


def apply_laplacian_filter(image, ksize=3):
    """Apply Laplacian filter for edge detection."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)


def apply_canny_edge_detector(image, threshold1=100, threshold2=200):
    """Apply Canny edge detector."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return cv2.Canny(image, threshold1, threshold2)


def apply_custom_kernel(image, kernel):
    """Apply a custom kernel to an image."""
    return cv2.filter2D(image, -1, kernel)
