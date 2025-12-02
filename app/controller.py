import logging
import threading
from utils.file_utils import get_files_list_in_path
from app.image_processor import load_image

logger = logging.getLogger(__name__)

class AppController:
    def __init__(self):
        self.selected_folder = None
        self.selected_filetype = "png"
        self.filetype_options = ["jpg", "jpeg", "png", "bmp"]
        self.processing_thread = None
        self.callback_progress = None
        self.callback_finished = None
    
    def set_selected_folder(self, folders):
        self.selected_folder = folders
    
    def set_progress_callback(self, callback):
        self.callback_progress = callback

    def set_finished_callback(self, callback):
        self.callback_finished = callback
    
    def process_images(self):
        if not self.selected_folder:
            logger.warning("No folders selected!")
            return

        if self.processing_thread and self.processing_thread.is_alive():
            logger.warning("Processing already running")
            return
        self.processing_thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.processing_thread.start()
    
    def _worker(self):
        files = get_files_list_in_path(self.selected_folder, self.selected_filetype)

        total = len(files)
        if total == 0:
            logger.info("No files found.")
            if(self.callback_finished):
                self.callback_finished()
            return

        for index, file in enumerate(files, start=1):
            full_path = f"{self.selected_folder}/{file}"

            try:
                img = load_image(full_path)
                print(f"Loaded {file}, shape={img.shape if img is not None else None}")
            except FileNotFoundError:
                logger.warning(f"File not found: {full_path}")
            
            if self.callback_progress:
                self.callback_progress(index, total, file)
        
        if self.callback_finished:
            self.callback_finished()