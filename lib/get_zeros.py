import numpy as np

def get_zeros(vet, delta):
  vet = np.asarray(vet)

  pos = np.where((vet >= -delta) & (vet <= delta))[0]


  zerocross = np.where(
    np.logical_xor(
      vet[:-1] > delta,
      vet[1:] > delta
    )
  )[0] + 1

  pos = np.concatenate((pos, zerocross))
  pos = np.sort(pos)
  
  if pos.size > 0:
    dif = pos[1:] - pos[:-1]

    # inicio dos blocos
    inicio = np.concatenate((
      [pos[0]],
      pos[np.where(dif > 1)[0] +1]
    ))

    # fim dos blocos
    fim = np.concatenate((
      pos[np.where(dif > 1)[0]],
      [pos[-1]]
    ))

    tam = fim - inicio + 1

    zeros = np.column_stack((inicio, fim, tam))
  else:
    zeros = np.empty((0, 3), dtype=int)

  return zeros