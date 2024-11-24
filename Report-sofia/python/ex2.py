import scipy as sp
import scipy.signal as sig
import numpy as np
from sympy import *
import matplotlib.pyplot as plt
# Import lambdify and I (imaginary unit) from SymPy
from sympy import symbols, simplify, lambdify, I

# Convert linear value to dB


def lin2dB(val):
    return 20*np.log10(val)


# Define the symbolic variables
vin, v1, vx, vo, s, vos1, vos2 = symbols(
    "V_{in} V_1 V_x V_o s V_{os1} V_{os2}")

# Passa-baixo


na = 58079
n = 1e-9
k = 1000

# Define the components
r1 = 3.33*k
r2 = 62.9*k
r3 = 120.8*k + k*(na/(470000))
r4 = 30*k + k*(na/1600)
r5 = 18*k
c1 = 0.9*n
c2 = 0.9*n
c3 = 40.7*n - n*(na/470000)

# Print the component values
print(f"R1 = {r1/k:.3f} K   ;R2 = {r2/k:.3f} K")
print(f"R3 = {r3/k:.3f} K   ;R4 = {r4/k:.3f} K")
print(f"R5 = {r5/k:.3f} K   ;C1 = {c1*1e9:.3f} n")
print(f"C2 = {c2*1e9:.3f} n   ;C3 = {c3*1e9:.3f} n")
print("\n")

# Define the impedances
z1 = 1/(s*c1)
z2 = 1/(s*c2)
z3 = 1/(s*c3)


# Stage 1

# V+ = Vin * R3/(R3 + Z3)
# If1 = V+/R5
# V1 - If1*R4 - V+ = 0

vp = vin * r3/(r3+z3)
if1 = vp/r5
s1 = solve(v1 - if1*r4 - vp, v1)

v1 = s1[0]  # output of the first stage

print("First Stage Output:")
pprint(v1)
# print the latex equation
print("\nLatex Eq.: \n"+latex(v1))

# Stage 2

# Vx = V1 - Vr1
# Vo = Z2/(Z2+R2) * Vx

saux = solve(vx*z2/(z2+r2) - vo, vx)
# pprint(saux)

vx = saux[0]

# vo = (vx - v1)/r1 + (vx)/(r2+z2) + (vx-vo)/z1
s2 = solve(
    (vx - v1)/r1 + (vx)/(r2+z2) + (vx-vo)/z1, vo)  # vo

vo = s2[0]  # output of the second stage

# Transfer function
Fs = simplify(vo / vin)

print("Filter Transfer Function: ")
pprint(Fs)

# print the latex equation
print("\nLatex Eq.: \n"+latex(Fs))


num, den = fraction(Fs)
z = solve(num, s)
p = solve(den, s)

print("Filter Zeros: ")
print(z)
print("Filter Poles: ")
print(p)
print("Frequency:")
for n in p:
    print(f"{abs(n)/(2*np.pi)}")

# Create a function for the transfer function
Fs_numeric = lambdify(s, Fs, 'numpy')

pmax = 6  # Maximum power of 10
pmin = -1  # Minimum power of 10

w = 2 * np.pi * np.logspace(pmin, pmax, 500)  # Frequency range

s_values = 1j * w  # Convert the frequency to the Laplace domain
h = Fs_numeric(s_values)  # Calculate the frequency response

# Find the frequency where the magnitude is 16.9 dB because it is the cutoff frequency
ind = np.where(np.isclose(20*np.log10(abs(h)), 16.9, atol=0.05))

print(ind)

# Plot the Bode diagram
plt.figure(figsize=(10, 8))

# Magnitude plot
plt.subplot(2, 1, 1)
plt.semilogx(w/(2*np.pi), 20 * np.log10(abs(h)))
plt.title('Bode Diagram')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.xlim(left=1e-1)

# Phase plot
plt.subplot(2, 1, 2)
plt.semilogx(w/(2*np.pi), np.angle(h, deg=True))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (degrees)')
plt.grid(True)
plt.xlim(left=1e-1)

plt.tight_layout()
plt.show()

# Find the maximum gain and the frequency where it occurs
MaxGain = max(abs(h))
# Find the position of the maximum gain
MaxPos = np.unravel_index(np.argmax(h), h.shape)
print("Max Gain: ", end="")
print(lin2dB(MaxGain))

# Find the frequency where the maximum gain occurs
print("Freq: ", end="")
print(w[MaxPos]/(2*np.pi))
