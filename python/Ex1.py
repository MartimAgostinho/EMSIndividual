from sympy import *

r1, r2, r3,r4, vi, vo, vp,vn, ibiasp,ibiasn = symbols("R_1 R_2 R_3 R_4 V_i V_o V_p V_n I_{BIAS+} I_{BIAS-}")

it = vi/r1
vx = vi + r2*it
i3 = it + vx/r4
vo1 = simplify(vx + r3*i3)

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
print( latex( vo2 ) )
vo2 = s2[0]

vo = vo1 + vo2

pprint(vo)