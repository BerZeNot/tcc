import tkinter as tk
from tkinter import Frame, Label, Button, filedialog

class MainWindow:
    def __init__(self, controller):
        self.controller = controller

        self.controller.set_progress_callback(self.on_progress)
        self.controller.set_finished_callback(self.on_finished)

        self.window = tk.Tk()
        self.window.title("App Prototype")

        self.selected_folder = None

        self.frame = Frame(self.window, padx=40, pady=40)
        self.frame.grid(column=1, row=1)
        
        Label(self.frame, text="Select a folder with images to process").grid(column=1, row=1, columnspan=2)

        self.folder_path_label = Label(self.frame, text="")
        self.folder_path_label.grid(column=1, row=2, columnspan=2)

        Button(self.frame, text="Select folder", command=self.select_folder).grid(column=1, row=4)
        Button(self.frame, text="Run", command=self.run_processing).grid(column=1, row=5)

        self.progress_label = Label(self.frame, text="")
        self.progress_label.grid(column=1, row=6, pady=10)

    def select_folder(self):
        path = filedialog.askdirectory(initialdir="/home/paulo")
        self.selected_folder = path
        self.folder_path_label.config(text=f"Selected folder: {path.split('/')[-1]}")
        self.controller.set_selected_folder(path)

    def run_processing(self):
        self.progress_label.config(text="Processing...")
        self.controller.process_images()

    def on_progress(self, index, total, filename):
        def update_label():
            self.progress_label.config(
                text=f"Processing {index}/{total}: {filename}"
            )

        self.window.after(0, update_label)

    def on_finished(self):
        def update_label():
            self.progress_label.config(text="Finished!")
        self.window.after(0, update_label)
    
    def run(self):
        self.window.mainloop()