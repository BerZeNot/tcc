import cv2
import os
import logging
import numpy as np

logger = logging.getLogger(__name__)

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


def rgb2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def gallus_segseq(imageInGrayScale, file):
    logger.info(f"[INFO]: Processing file '{file}'")
    logger.info(f"[INFO]: Image shape: {imageInGrayScale.shape}")
    logger.info("[INFO]: Aplicando algoritmo de gallus_segseq")


def write_image(path, img):
    logger.info(f"[INFO]: writing image in path '{path}'")
    return cv2.imwrite(path, img)