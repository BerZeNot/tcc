import cv2
import os
import numpy as np

def load_image(full_path: str): 
    if not os.path.exists(full_path):
        raise FileExistsError("File not exists")

    img = cv2.imread(full_path)
    return assert_rgb_image(img)


# Asserts that the img is RGB:
# if is grayscale, converts to RGB
# else returns the original image 
def assert_rgb_image(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        return img
    return img

# Cut image edges in percentage%
def cut_edges(img, percentage):
    height, width = img.shape[:2]

    cut_height = int(np.floor(height * (percentage / 100)))
    cut_width  = int(np.floor(width  * (percentage / 100)))

    newImg = img[
        cut_height:height - cut_height,
        cut_width:width - cut_width
    ]
    return newImg

def write_image(path, img):
    return cv2.imwrite(path, img)