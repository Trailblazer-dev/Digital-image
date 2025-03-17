import cv2
import numpy as np
from scipy import ndimage
from skimage import transform


def fourier_transform(image):
    """Apply Fourier transform to an image."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    f_transform = np.fft.fft2(image)
    f_shift = np.fft.fftshift(f_transform)
    magnitude_spectrum = 20 * np.log(np.abs(f_shift) + 1)
    
    return f_transform, f_shift, magnitude_spectrum


def inverse_fourier_transform(f_shift):
    """Apply inverse Fourier transform."""
    f_ishift = np.fft.ifftshift(f_shift)
    img_back = np.fft.ifft2(f_ishift)
    return np.abs(img_back)


def histogram_equalization(image):
    """Apply histogram equalization to improve contrast."""
    if len(image.shape) == 3:
        # For color images, apply equalization to the Y channel in YUV space
        img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    else:
        # For grayscale images
        return cv2.equalizeHist(image)


def warp_perspective(image, points1, points2, output_size=None):
    """Apply perspective transformation using four point correspondences."""
    if output_size is None:
        output_size = (image.shape[1], image.shape[0])
    
    M = cv2.getPerspectiveTransform(points1, points2)
    return cv2.warpPerspective(image, M, output_size)


def affine_transform(image, points1, points2):
    """Apply affine transformation using three point correspondences."""
    M = cv2.getAffineTransform(points1, points2)
    return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
