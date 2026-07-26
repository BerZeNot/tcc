import numpy as np


def Symmetry(image, mirror):

    joint = image + mirror

    a1 = np.count_nonzero(image)
    a2 = np.count_nonzero(mirror)
    a3 = np.count_nonzero(joint == 2)

    denom = a1 + a2 - a3

    if denom == 0:
        symmetry = 0.0
    else:
        symmetry = a3 / denom

    return symmetry, joint
