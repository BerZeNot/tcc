import cv2
import numpy as np

from lib.calc_dist_point_line_no_abs import CalcDistPointLineNoABS


def MirrorIm(image, point_on_line, direction):

    rows, cols = np.where(image == 1)

    points = np.column_stack((rows, cols))

    distances = CalcDistPointLineNoABS(
        point_on_line,
        direction,
        points,
    )

    mirrored = np.round(
        points + 2 * distances[:, None] * np.array([-direction[1], direction[0]])
    ).astype(int)

    out = np.zeros_like(image)

    valid = (
        (mirrored[:, 0] >= 0)
        & (mirrored[:, 0] < image.shape[0])
        & (mirrored[:, 1] >= 0)
        & (mirrored[:, 1] < image.shape[1])
    )

    mirrored = mirrored[valid]

    out[
        mirrored[:, 0],
        mirrored[:, 1],
    ] = 1

    se = np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        dtype=np.uint8,
    )

    out = cv2.dilate(out.astype(np.uint8), se)
    out = cv2.erode(out, se)

    return out
