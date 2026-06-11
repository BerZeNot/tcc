import numpy as np

def follow(img, nhood=8):
    if nhood == 8:
        path = np.array([
            [ 0,  1],
            [-1,  1],
            [-1,  0],
            [-1, -1],
            [ 0, -1],
            [ 1, -1],
            [ 1,  0],
            [ 1,  1]
        ])

        cane = 4 
        nxt = np.array([1,2,3,4,5,6,7,0])
        inv = np.array([4,5,6,7,0,1,2,3])

    elif nhood == 4:
        path = np.array([
            [-1, 0],
            [ 0, 1],
            [ 1, 0],
            [ 0,-1]
        ])

        cane = 3
        nxt = np.array([1,2,3,0])
        inv = np.array([2,3,0,1])

    else:
        raise ValueError("Invalid neighborhood number")
    
    img = np.pad(img, 1)

    idx = np.flatnonzero(img == 1)[0]

    rows = img.shape[0]

    j = idx // rows
    i = idx - j * rows

    neighbours = np.zeros_like(path)
    neighbours[:, 0] = path[:, 0] + i
    neighbours[:, 1] = path[:, 1] + j

    x = []
    y = []

    start_i = i
    start_j = j

    finished = False

    while not finished:
        x.append(j - 2)
        y.append(rows - 2 - i)

        cini = cane
        while True:
            cane = nxt[cane]

            ni = neighbours[cane, 0]
            nj = neighbours[cane, 1]

            if img[ni, nj] != 0 or cane == cini:
                break
        
        ni = neighbours[cane, 0]
        nj = neighbours[cane, 1]

        if img[ni, nj] == 1:

            di, dj = path[cane]

            i += di
            j += dj

            neighbours[:, 0] += di
            neighbours[:, 1] += dj

            cane = inv[cane]

            finished = (i == start_i and j == start_j)
        
        else:
            finished = True

    return np.asarray(x), np.asarray(y)