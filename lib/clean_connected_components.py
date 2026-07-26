from lib.clear_border import clear_border
from lib.cleancc import cleancc

"""
cleans connected components for gallus sperma images
"""


def clean_connected_components(image_seg_clean_g, min_size, max_size, border=0):
    # remove 1 pixel from the border to avoid border problems
    imc = clear_border(image_seg_clean_g, 1)

    # removes undesired connected components
    res = cleancc(imc, min_size, max_size, border)
    return res
