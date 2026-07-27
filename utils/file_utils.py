import os
import os.path as path


def get_files_list_in_path(path: str, file_extension: str):
    file_list = os.listdir(path)
    file_list_filtered_by_file_extension = [
        file for file in file_list if file.split(".")[-1] == file_extension
    ]

    return file_list_filtered_by_file_extension


def create_folder(base_path: str, folder_name: str):
    full_path = path.join(base_path, folder_name)
    os.mkdir(full_path)
