import numpy as np
from lib.get_zeros import get_zeros

def get_mountains(vector, buf):
    vector = np.asarray(vector)

    # normalização
    vecd = vector / (np.max(vector) - np.min(vector))

    # zerando as bordas
    vecd[:buf] = 0
    vecd[-buf:] = 0

    # regiões de zero
    zeros = get_zeros(vecd, 1e-4)

    p1 = zeros[:-1, 1]
    p2 = zeros[1:, 0]

    mon = np.zeros_like(vecd, dtype=int)

    mon_max = []
    mon_max_pos = []

    # montanhas iniciais
    for ip in range(len(p1)):
        val = vector[p1[ip]:p2[ip] + 1]

        mmaxpos = np.argmax(np.abs(val))
        mmax = np.abs(val[mmaxpos])

        mon_max.append(mmax)
        mon_max_pos.append(p1[ip] + mmaxpos)
    
    mon_max = np.asarray(mon_max)
    mon_max_pos = np.asanyarray(mon_max_pos)

    #ordenação decrescente
    k = np.argsort(mon_max)[::-1]

    mon_max = mon_max[k]
    mon_max_pos = mon_max_pos[k]

    # montanhas ordenadas
    for ip in range(len(p1)):
        mon[p1[k[ip]]:p2[k[ip]]+1] = ip + 1
    
    return mon, mon_max, mon_max_pos