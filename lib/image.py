import cv2
from cv2.typing import MatLike

def image_adjust(image: MatLike) -> MatLike:
    return cv2.convertScaleAbs(image, alpha=1.2, beta=20)

def apply_gausian_filter(image, sigma):
    return cv2.GaussianBlur(image, (sigma, sigma), 0)

def normalize_histogram_spread(image: MatLike) -> MatLike:
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)