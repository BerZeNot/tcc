import numpy as np

def entropy(image, n):
    f, _ = np.histogram(image, bins=np.arange(n + 2))
    f = f[f != 0]
    sfi = f / np.sum(f)
    h = -np.sum(sfi * np.log2(sfi))
    return h