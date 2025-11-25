import cv2
import os

def read_image(full_path: str): 
    if not os.path.exists(full_path):
        raise FileExistsError("File not exists")
    return cv2.imread(full_path)

def get_files_list_in_path(path: str, file_extension: str):
    file_list = os.listdir(path)
    file_list_filtered_by_file_extension = [
        file for file in file_list 
            if file.split(".")[-1] == file_extension]

    return file_list_filtered_by_file_extension
