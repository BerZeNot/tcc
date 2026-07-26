import numpy as np


def drawline(img, point_on_line, direction, value):
    """
    Draws a line starting from point_on_line in the direction of `direction`
    until the image border is reached.

    Parameters
    ----------
    img : np.ndarray
        Input image.
    point_on_line : array-like
        Starting point [row, col].
    direction : array-like
        Direction vector.
    value : float or int
        Pixel value to draw.

    Returns
    -------
    np.ndarray
    """

    tx, ty = img.shape

    direction = np.asarray(direction, dtype=np.float64)
    point_on_line = np.asarray(point_on_line, dtype=np.float64)

    norm = np.linalg.norm(direction)
    if norm == 0:
        return img.copy()

    direction /= norm

    pts = []

    i = 0
    while True:

        p = point_on_line + direction * i

        if p[0] < 2 or p[0] > tx - 1 or p[1] < 2 or p[1] > ty - 1:
            break

        pts.append(np.round(p).astype(int))

        i += 0.5

    out = img.copy()

    if pts:
        pts = np.asarray(pts)
        out[pts[:, 0], pts[:, 1]] = value

    return out
