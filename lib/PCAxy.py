import numpy as np

def PCAxy(x, y):
    # matriz de covariância
    M = np.array([
        [np.cov(x, x, bias=False)[0, 1], np.cov(x, y, bias=False)[0, 1]],
        [np.cov(y, x, bias=False)[0, 1], np.cov(y, y, bias=False)[0, 1]]
    ])

    # autovalores e autovetores
    aVal, aVec = np.linalg.eig(M)

    # ordenação em ordem decrescente dos autovalores
    idx = np.argsort(aVal)[::-1]
    aVal = aVal[idx]
    aVec = aVec[:, idx]

    return aVal, aVec