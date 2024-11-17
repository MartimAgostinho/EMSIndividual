import scipy.signal as sig
import numpy as np
import math
import matplotlib.pyplot as plt 
from sympy import *


k       = 1000
Blue    = (       0, 101/255, 189/255 )
Green   = (  52/255, 129/255,  65/255 )
Orange  = ( 241/255,  89/255,  41/255 )

CuttoffFreq = 392
Fs          = 80*k
Ts          = 1/Fs
wc          = CuttoffFreq*2*np.pi
ws          = Fs*2*np.pi 

order       = 400    #TODO: Get order

order = math.ceil(order)
if order % 2 == 0:
    order += 1

window = 'blackman' #TODO descobrir a window

filter = sig.firwin(
            order,
            cutoff      = wc, 
            window      = window, 
            pass_zero   = True, 
            scale       = True,
            fs          = ws
                )

w,h = sig.freqz(filter)
w   = w/(Ts*2*np.pi)
mag = 20*np.log10( abs(h) )
pha = np.angle( h,deg=True )   

#Find cuttoff freq

cutoff_idx       = np.where(mag <= 20*np.log10( abs(h[0]) )-3.01)[0][0]
cutoff_frequency = w[cutoff_idx]
print( cutoff_frequency )

# Magnitude response
plt.subplot(2, 1, 1)
plt.semilogx(w, mag,color = Blue)
plt.axvline(x=cutoff_frequency, color=Green, linestyle='--', linewidth=1,label="Cutoff Frequency")
plt.title('Bode Magnitude Plot ')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()

# Bode Phase response
plt.subplot(2, 1, 2)
plt.semilogx(w, pha,color=Blue)
plt.xlabel('Frequency (rad/s)')
plt.ylabel('Phase (degrees)')
plt.grid(True)
plt.legend()
plt.show()

print("\nFIR Coefs: ")
out = ''
for c in filter:
    out += str(c) + ", "
out = out[:-2]
print(out)