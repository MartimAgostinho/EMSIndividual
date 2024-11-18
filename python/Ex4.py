import scipy.signal as sig
import numpy as np
import math
import matplotlib.pyplot as plt 
from sympy import *

k       = 1000
Blue    = (       0, 101/255, 189/255 )
Green   = (  52/255, 129/255,  65/255 )
Orange  = ( 241/255,  89/255,  41/255 )

Fs = 80*k * 2*np.pi

numz    = [ 0.8,6*0.8,0.8 ]
denz    = [1, -0.36953, 0.19582]
wz, hz  = sig.freqz(numz, denz,fs=Fs)

z,p,k   = sig.tf2zpk(numz,denz)
print("Zeros:" ,end="")
print(z)
print("Poles:" ,end="")
print(p)
print("Gain: ",end='')
print(k)
print("Gain DC: ",end='')
print( 20*np.log10( hz[0] ) )

magnitude_db = 20 * np.log10(abs(hz))

cutoff_idx       = np.where(magnitude_db <= 20*np.log10( hz[0] )-3.01)[0][0]
cutoff_frequency = wz[cutoff_idx] / (2 * np.pi) 
print( cutoff_frequency )


# Magnitude response
plt.subplot(2, 1, 1)
plt.semilogx(wz/(2*np.pi), 20*np.log10(abs(hz)),color=Blue)
plt.axvline(x=cutoff_frequency, color=Green, linestyle='--', linewidth=1)
plt.title('Bode Magnitude Plot ')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()

# Bode Phase response
plt.subplot(2, 1, 2)
plt.semilogx(wz/(2*np.pi), np.angle(hz,deg=True),color = Blue)
plt.xlabel('Frequency (rad/s)')
plt.ylabel('Phase (degrees)')
plt.grid(True)
plt.legend()
plt.show()
