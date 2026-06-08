from enum import Enum
import numpy as np

class Domain(Enum):
   TIME = "time"
   FREQUENCY = "frequency"
   COMPLEX = "complex"


def fftderiv(
   y, n=1, sigma=5, delta=1,
   input_domain=Domain.TIME,
   output_domain=Domain.TIME
):
   y = np.asarray(y)

   # garante vetor linha
   if y.ndim > 1 and y.shape[1] < y.shape[0]:
      y = y.T
   
   N = y.shape[-1]

   if input_domain == Domain.TIME: 
      delta = 1

      Y = np.fft.fft(y)

      dt = delta
      aux = 1 / dt
      df = 1 / (N * dt)

   elif input_domain == Domain.FREQUENCY: 
      delta = 1 / N

      Y = y

      df = delta
      aux = N * df
      dt = 1 / aux

   else:
      raise ValueError(
         "input_domain' must be Domain.TIME"
         "or Domain.FREQUENCY'"
      )
   
   # eixo de frequências
   f = np.arange(N) * df

   f[int(np.floor(N / 2)):] -= aux

   # gausiana no domínio da frequência
   if sigma == 0:
      G = np.ones_like(y, dtype=float)
   else:
      G = np.exp(-2 * (sigma * np.pi * f) ** 2)
   
   # derivada no domínio da frequência
   DY = Y * G * (1j * 2 * np.pi * f) ** n

   # saída
   if output_domain == Domain.TIME:
      Dy = np.real(np.fft.ifft(DY))
   
   elif output_domain == Domain.COMPLEX:
      Dy = np.fft.ifft(DY)
   
   elif output_domain == Domain.FREQUENCY:
      Dy = DY
   
   else:
      raise ValueError(
         "'output_domain' must be"
         "Domain.TIME, Domain.FREQUENCY' "
         "or Domain.COMPLEX"
      )

   return Dy, DY