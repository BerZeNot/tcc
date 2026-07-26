from lib.drawline import drawline


def DrawPCAVectors(image, center_of_mass, eigenvectors):

    image = drawline(
        image,
        center_of_mass,
        eigenvectors[:, 0],
        0.5,
    )

    image = drawline(
        image,
        center_of_mass,
        eigenvectors[:, 1],
        0.5,
    )

    return image
