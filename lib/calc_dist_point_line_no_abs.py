import numpy as np


def CalcDistPointLineNoABS(point_on_line, direction, points):
    """
    Signed distance from each point to a line.
    """

    direction = np.asarray(direction, dtype=np.float64)
    point_on_line = np.asarray(point_on_line, dtype=np.float64)
    points = np.asarray(points, dtype=np.float64)

    ap = points - point_on_line

    numerator = ap[:, 0] * direction[1] - ap[:, 1] * direction[0]

    denominator = np.linalg.norm(direction)

    return numerator / denominator
