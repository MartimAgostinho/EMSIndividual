import scipy as sp 
import scipy.signal as sig
import numpy as np
from sympy import *
import matplotlib.pyplot as plt 
from sympy import symbols, simplify, lambdify, I  # Import lambdify and I (imaginary unit) from SymPy

def lin2dB(val):
    return 20*np.log10(val)

vin, v1, vx, vo, s = symbols("V_{in} V_1 V_x V_o s")

#Passa-baixo

na = 70386
n  = 1e-9
k  = 1000

r1 = 3.33*k
r2 = 62.9*k
r3 = 120.8*k + k*na/(470000) 
r4 = 30*k + k*na/1600
r5 = 18*k
c1 = 0.9*n
c2 = 0.9*n
c3 = 40.7*n - n*na/470000

print(f"R1 = {r1/k:.3f} K   ;R2 = {r2/k:.3f} K")
print(f"R3 = {r3/k:.3f} K   ;R4 = {r4/k:.3f} K")
print(f"R5 = {r5/k:.3f} K   ;C1 = {c1*1e9:.3f} n")
print(f"C2 = {c2*1e9:.3f} n   ;C3 = {c3*1e9:.3f} n")
print("\n")
z1 = 1/(s*c1)
z2 = 1/(s*c2)
z3 = 1/(s*c3)


#Stage 1

vp  = vin* r3/(r3+z3)
if1 = vp/r5
s1  = solve( v1 - if1*r4 - vp,v1)
v1  = simplify(s1[0])

print("\nFirst Stage Output:")
pprint(v1)
print("\nLatex Eq.: \n"+latex(v1))

#Stage 2

v1 = symbols("V_1")
# Vx = V1 - Vr1
saux = solve( vx*z2/(z2+r2) - vo,vx )
#pprint(saux)
vx = saux[0]

s2 = solve( 
    (vx - v1)/r1 + (vx)/(r2+z2) + (vx-vo)/z1
    ,vo)[0]

Fs = simplify( s2 )

print("\nSecond Stage:")
pprint(Fs)
print("\nLatex: \n"+latex(Fs))

Fs = simplify(Fs.subs(v1,s1[0])/vin)
print( "\nFilter Transfer Function: " )
pprint(Fs)
print("\nLatex Eq.: \n"+latex(Fs))


num,den = fraction(Fs)
z       = solve( num,s )
p       = solve( den,s )

print("\n\nFilter Zeros: ")
print(z)
print("Filter Poles: ")
print(p)
print("Frequency:")
for n in p:
    print( f"{abs(n)/(2*np.pi)}" )
 
Fs_numeric = lambdify(s, Fs, 'numpy')

pmax = 6
pmin = 0

freqs  = np.logspace(pmin, pmax, 500)
w = 2 * np.pi * freqs

s_values = 1j * w 
h = Fs_numeric(s_values) 

MaxGain = max(abs(h))
MaxPos  = np.unravel_index(np.argmax(h),h.shape)
print("Max Gain: ",end="")
print(lin2dB(MaxGain))
print("Freq: ",end="")
print( w[MaxPos]/(2*np.pi) )

ind = np.where(np.isclose(20*np.log10(abs(h)), lin2dB(MaxGain) - 3.01, atol=0.1))
print("CutOff Freqs:")
print(freqs[ind])

plt.figure(figsize=(10, 8))
# Magnitude plot
plt.subplot(2, 1, 1)
plt.semilogx(freqs, 20 * np.log10(abs(h)))  # Convert magnitude to dB
plt.axvline( 10*k,linestyle="--" )
plt.scatter(
    [(w/(2*np.pi))[150], (w/(2*np.pi))[286] ],
    [20*np.log10(abs(h[150])),20*np.log10(abs(h[286]))] ,
     marker='x', color='black', label='Poles')
plt.title('Bode Diagram')
plt.ylabel('Magnitude (dB)')
plt.grid(True)

# Phase plot
plt.subplot(2, 1, 2)
plt.semilogx(freqs, np.angle(h, deg=True))  # Phase in degrees
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (degrees)')
plt.grid(True)

plt.tight_layout()
plt.show()
