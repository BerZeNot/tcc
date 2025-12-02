import cv2
import os

def load_image(full_path: str): 
    if not os.path.exists(full_path):
        raise FileExistsError("File not exists")
    return cv2.imread(full_path)
