import os
from pathlib import Path

USER_HOME_DIR = str(Path.home())

DEFAULT_IMAGE_FORMAT = "bmp"

SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "bmp"]

WINDOW_TITLE = "App Prototype"

OUTPUT_FOLDER_BASE_NAME = "processed_images"

DEFAULT_FOLDERS = ["heads", "valid_heads", "auxiliary_files"]
