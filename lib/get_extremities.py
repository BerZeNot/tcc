import numpy as np


def GetExtremities(image, center_of_mass, direction):
    """
    Measures the object's extent along the given direction.
    """

    direction = np.asarray(direction, dtype=np.float64)

    direction /= np.linalg.norm(direction)

    p1 = np.asarray(center_of_mass, dtype=np.float64)
    p2 = np.asarray(center_of_mass, dtype=np.float64)

    r = np.round(p1).astype(int)

    while (
        0 <= r[0] < image.shape[0]
        and 0 <= r[1] < image.shape[1]
        and image[r[0], r[1]] != 0
    ):
        p1 += direction * 0.5
        r = np.round(p1).astype(int)

    r = np.round(p2).astype(int)

    while (
        0 <= r[0] < image.shape[0]
        and 0 <= r[1] < image.shape[1]
        and image[r[0], r[1]] != 0
    ):
        p2 -= direction * 0.5
        r = np.round(p2).astype(int)

    return np.linalg.norm(p2 - p1)
