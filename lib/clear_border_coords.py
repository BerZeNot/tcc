def clear_border_coords(image, top, left, bottom, right, new_value=0):
    response = image.copy()

    if top > 0:
        response[:top, ...] = new_value
    
    if bottom > 0:
        response[-bottom:, ...] = new_value

    if left > 0:
        response[:, :left, ...] = new_value
    
    if right > 0:
        response[:, -right:, ...] = new_value
    
    return response