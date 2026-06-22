import numpy as np

def getbb(img, val, inc, inctxty=False):
    """
    Obtém a bounding box do objeto com rótulo `val`.

    Parâmetros
    ----------
    img : ndarray
        Imagem rotulada (resultado de connected components).
    val : int
        Valor do rótulo desejado.
    inc : int ou float
        Incremento da borda.
    inctxty : bool
        Se True, o incremento é proporcional ao tamanho do objeto.

    Retorna
    -------
    im : ndarray
        Imagem contendo apenas o objeto dentro da bounding box expandida.
    index : tuple(ndarray, ndarray)
        Índices dos pixels do objeto na imagem original.
    origin : ndarray
        Origem da bounding box.
    """

    index = np.where(img == val)

    x, y = index
    maxx, minx = x.max(), x.min()
    maxy, miny = y.max(), y.min()

    tx = maxx - minx + 1
    ty = maxy - miny + 1

    if inctxty:
        ntx = int(tx + 2 * inc * tx)
        nty = int(ty + 2 * inc * ty)

        row = (x - minx + inc * tx).astype(int)
        col = (y - miny + inc * ty).astype(int)
        
    else:
        ntx = tx + 2 * inc
        nty = ty + 2 * inc

        row = x - minx + inc
        col = y - miny + inc
    
    im = np.zeros((int(ntx), int(nty)), dtype=np.uint8)
    im[row, col] = 1

    origin = np.array([minx - tx - 1, miny - ty - 1])

    return im, index, origin