from sympy import *

r1, r2, r3,r4, vi, vo, vp,vn, ibiasp,ibiasn, vy, vout = symbols("R_1 R_2 R_3 R_4 V_i V_o V_p V_n I_{BIAS+} I_{BIAS-} V_y V_{out}")

it = vi/r1
vx = vi + r2*it
i3 = it + vx/r4
vo1 = simplify(vx + r3*i3)

vout = (-(r3*r2 + r2*r4 + r3*r4) / (r4*r1))

pprint(vout)
print(latex(vout)) #ganho em montagem inversora

pprint(simplify(vo1))
print( latex(vo1) )


#Ibias 
ir1, ir3, ir4, it,vx = symbols("I_{R1} I_{R3} I_{R4} I_t V_x")
#vx  = vo - ir3*r3
eq2 = Eq( vx/r4 + (vx - vo)/r3 + ibiasn,0 )
s3  = solve(eq2,vx)
vx  = s3[0] 
eq1 = Eq( vo - (vx - vo)*r3,ibiasn*r2 )
pprint(eq1)
s2  = solve(eq1,vo)
pprint(simplify(s2[0]))
#print( latex( vo2 ) )
#vo2 = s2[0]

#vo = vo1 + vo2

#pprint(vo)

#ruido
vo1r, vo2r, vo3r, vo4r, vo5r, vo6r, vo7r, vor, vnamp = symbols("V_{OR1} V_{OR2} V_{OR3} V_{OR4} V_{OR5} V_{OR6} V_{OR7} V_{OR} V_{N_opamp}")
vr1r, vr2r, vr3r, vr4r, vir, ipr, inr = symbols("V_{R1_nrms} V_{R2_nrms} V_{R3_nrms} V_{R4_nrms} V_{In_nrms} I_{Inp_nrms} I_{Inn_nrms}")

vo1r = vout * vr1r
vo2r = vr2r * (1 + r3/r4)
vo3r = vr3r 
vo4r = vr4r * (1 + r3/r4)
vo5r = vir * vo1/vi
vo6r = inr + simplify((r1*vout*r1)/(r1 + vout*r1))
vo7r = vnamp

print(latex(vo7r))
pprint(vo5r)
pprint(vo6r)