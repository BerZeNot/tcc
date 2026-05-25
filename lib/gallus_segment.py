from cv2.typing import MatLike
from lib.get_mountains import get_mountains

def gallus_segment(image) :
    # Autor: Bruno A. N. Travençolo
    # FACOM - UFU
    # Data: 21/07/2010 last update 05/10/2011
    # Função:
    #   Segmentação de imagens de espermatozóides utilizando o primeiro
    #   pico da segunda derivada do histograma

    # Histograma
    # buffer de 15 pontos no histograma que serão zerados posteriormente
    # no cálculo da derivada
    buf=15
    h=histc(reshape(image,1,numel(image)),0-buf:255+buf)
    h = h/max(h(:))

    # o ponto de threshold será o máximo da segunda derivada do histograma
    n=2
    sigma=3
    [dh2,DY] = fftderiv(h,n,sigma)

    #zerando as pontas da derivada para remover ruídos
    dh2(1:buf) = 0
    dh2(end-buf:end) = 0
    dh2 = dh2./max(dh2(:))

    # dividindo a derivada em trechos de montanhas
    # isto é, de zero até uma valor máximo (ou mínimo) e de volta ao zero
    # mon - divisão da curva
    # mon_max - picos da curva (inclui negativos)
    # mon_max_pos -  posição dos picos nas curvas
    [mon, mon_max, mon_max_pos]=get_mountains(dh2,buf)

    # dentre os três primeiros picos mais altos, o desejado é o
    # que tem a menor coordenada no eixo x
    if (numel(mon_max_pos)==2)
        thr = min(mon_max_pos(1:2))
    else
    thr = min(mon_max_pos(1:3))
    end

    
    thr = thr - buf

    # segmentando
    im_seg = (image < (thr) )*1
