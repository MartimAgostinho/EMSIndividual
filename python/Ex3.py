import scipy.signal as sig
import numpy as np
import math
import matplotlib.pyplot as plt 
from sympy import *


k           = 1000

CuttoffFreq = 392
Fs          = 80*k
Ts          = 1/Fs
wc          = CuttoffFreq*2*np.pi
ws          = Fs*2*np.pi 

order       = 1000    #TODO: Get order

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
# Magnitude response
plt.subplot(2, 1, 1)
plt.semilogx(w, mag)
plt.title('Bode Magnitude Plot ')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()

# Bode Phase response
plt.subplot(2, 1, 2)
plt.semilogx(w, pha)
plt.xlabel('Frequency (rad/s)')
plt.ylabel('Phase (degrees)')
plt.grid(True)
plt.legend()
plt.show()