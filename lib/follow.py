import cv2
import numpy as np


def follow(image: np.ndarray):
    """
    Extrai o contorno externo de um objeto binário.

    Parameters
    ----------
    image : np.ndarray
        Imagem binária contendo valores 0 e 1 (ou 0 e 255).

    Returns
    -------
    x : np.ndarray
        Coordenadas x do contorno.
    y : np.ndarray
        Coordenadas y do contorno (origem no canto inferior esquerdo,
        compatível com a implementação original em Octave).
    """

    binary = (image != 0).astype(np.uint8)

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE,
    )

    if not contours:
        return np.empty(0, dtype=np.int32), np.empty(0, dtype=np.int32)

    contour = contours[0][:, 0]

    x = contour[:, 0]
    y = binary.shape[0] - 1 - contour[:, 1]

    return x, y
