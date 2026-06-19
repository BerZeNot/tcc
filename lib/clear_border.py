from lib.clear_border_coords import clear_border_coords

def clear_border(image, value, new_value=0):
    return clear_border_coords(
        image,
        top=value,
        left=value,
        bottom=value,
        right=value,
        new_value=new_value
    )