import numpy as np
from scipy import ndimage

def cleancc(image, min_size, max_size, border=0):
    """
    Remove componentes conexos menos que min_size,
    maiores que max_size ou que tocam a borda.

    Retorna a imagem rotulada filtrada.
    """

    bw_image, _ = ndimage.label(
        image, 
        structure=ndimage.generate_binary_structure(2, 1)
    )

    counts = np.bincount(bw_image.ravel())

    undes = np.where(
        (counts <= min_size) |
        (counts >= max_size)
    )[0]

    if border > 0:

        v1 = bw_image[:border, :]
        v2 = bw_image[-border:, :]
        v3 = bw_image[:, :border]
        v4 = bw_image[:, -border:]

        border_ids = np.unique(
            np.concatenate([
                v1.ravel(),
                v2.ravel(),
                v3.ravel(),
                v4.ravel()
            ])
        )

        undes = np.unique(
            np.concatenate([
                undes,
                border_ids
            ])
        )

    if len(undes) > 0:
        mask = np.isin(bw_image, undes)

        imc = bw_image.copy()
        imc[mask] = 0
    else:
        imc = bw_image

    return imc