import scipy.signal as sig
import numpy as np
import math
import matplotlib.pyplot as plt 
from sympy import *

k  = 1000
Fs = 80*k

numz    = [ 0.8,6*0.8,0.8 ]
denz    = [1, -0.36953, 0.19582]
wz, hz  = sig.freqz(numz, denz)

# Magnitude response
plt.subplot(2, 1, 1)
plt.semilogx(wz, 20*np.log10(abs(hz)))
plt.title('Bode Magnitude Plot ')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()

# Bode Phase response
plt.subplot(2, 1, 2)
plt.semilogx(wz, np.angle(hz,deg=True))
plt.xlabel('Frequency (rad/s)')
plt.ylabel('Phase (degrees)')
plt.grid(True)
plt.legend()
plt.show()
