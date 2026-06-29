import numpy as np
from lib.follow import follow


def perim(img):
    x, y = follow(img)

    dx = np.diff(x)
    dy = np.diff(y)

    p = np.sum(np.hypot(dx, dy))

    p += np.hypot(x[-1] - x[0], y[-1] - y[0])

    return float(p)
