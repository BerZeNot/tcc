import logging

from utils.file_utils import read_image
logger = logging.getLogger(__name__)

full_path = "/home/paulo/Pictures/Wallpapers/arch-linux-wallpaper.jpg"

try:
    img = read_image(full_path)
    print(img)
except FileExistsError:
    logger.warning("Skipping not found file: {full_path}") 
    # Maybe write or save some log for reporting fail details on interface.
