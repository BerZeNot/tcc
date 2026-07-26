import cv2
import numpy as np


def bull_erodedilate(image, n=3):
    """
    Remove a cauda do espermatozoide por meio de erosão seguida de dilatação.

    Parameters
    ----------
    image : np.ndarray
        Imagem binária.
    n : int, optional
        Número de iterações de erosão e dilatação.

    Returns
    -------
    np.ndarray
        Imagem binária resultante.
    """

    # elemento estruturante em cruz
    se = np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        dtype=np.uint8,
    )

    image_to_dilate = (image > 0).astype(np.uint8)

    # erosão
    image_to_dilate = cv2.erode(
        image_to_dilate,
        se,
        iterations=n,
    )

    # dilatação
    image_to_dilate = cv2.dilate(
        image_to_dilate,
        se,
        iterations=n,
    )

    # garante que a dilatação não ultrapasse a segmentação original
    image_to_dilate = image_to_dilate * (image > 0).astype(np.uint8)

    return (image_to_dilate > 0).astype(np.uint8)
