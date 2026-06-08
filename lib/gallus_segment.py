import numpy as np

from cv2.typing import MatLike
from lib.get_mountains import get_mountains
from lib.fftderiv import fftderiv

def gallus_segment(image: MatLike): 
    # buffer usado nas bordas do histograma
    buf=15

    # histograma
    bins = np.arange(0 - buf, 256 + buf + 1)

    h, _ = np.histogram(image.ravel(), bins=bins)

    h = h.astype(np.float64)
    h = h / np.max(h)

    # o ponto de threshold será o máximo da segunda derivada do histograma
    n = 2
    sigma = 3
    dh2, DY = fftderiv(h, n, sigma)

    #zerando as pontas da derivada para remover ruídos
    dh2[:buf] = 0
    dh2[-buf:] = 0

    dh2 = dh2 / np.max(dh2)

    # dividindo a derivada em trechos de montanhas
    # isto é, de zero até uma valor máximo (ou mínimo) e de volta ao zero
    # mon - divisão da curva
    # mon_max - picos da curva (inclui negativos)
    # mon_max_pos -  posição dos picos nas curvas
    [mon, mon_max, mon_max_pos]=get_mountains(dh2,buf)

    # dentre os três primeiros picos mais altos, o desejado é o
    # que tem a menor coordenada no eixo x
    if len(mon_max_pos) == 2:
        thr = np.min(mon_max_pos[:2])
    else:
        thr = np.min(mon_max_pos[:3])
    
    # compensação do buffer
    thr = thr - buf

    # segmentando
    im_seg = (image < thr).astype(np.uint8)
    
    return im_seg, thr
