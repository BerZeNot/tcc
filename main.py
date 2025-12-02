import tkinter as tk
from tkinter import Frame, Label, Button, filedialog
import logging
from utils.file_utils import read_image, get_files_list_in_path

logger = logging.getLogger(__name__)
selected_folder_path = None
filetype = "jpg"
def select_folder():
    global selected_folder_path
    path = filedialog.askdirectory(initialdir="/home/paulo")
    selected_folder_path = path
    folder_name = path.split("/")[-1]
    selected_folder_details_text = f"Selected folder: {folder_name}"
    folder_path_label.config(text=selected_folder_details_text)

def exec_file_reading():

    global selected_folder_path
    found_files = get_files_list_in_path(selected_folder_path, filetype)
    if not found_files:
        logger.info(f"No files of type {filetype} found in the directory {selected_folder_path}")
        return

    for file_name in found_files:
        try:
            print(f"Trying to read file {file_name}...")
            img = read_image(f"{selected_folder_path}/{file_name}")
            print(img[0])
        except FileExistsError:
            logger.warning("Skipping not found file: {full_path}") 
            # Maybe write or save some log for reporting fail details on interface.

window = tk.Tk()

frame = Frame(window, padx=40, pady=40).grid(column=1, row=1)

Label(frame, text="Select a folder with images to process", pady=10, padx=10).grid(column=1, row=1, columnspan=2)
folder_path_label = Label(frame, text="", pady=10, padx=10)
folder_path_label.grid(column=1, row=2, columnspan=2)

buton_select_folder = Button(frame, text="Select folder", command=select_folder).grid(column=1, row=4, columnspan=3)
buton_run = Button(frame, text="Run", command=exec_file_reading).grid(column=1, row=5, columnspan=3)
window.title("App Prototype")
window.mainloop()

