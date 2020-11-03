# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 20:48:30 2020

@author: Hakan İbrahim Tol, PhD

References: 
[1] Pálsson, Hálldór. Methods for planning and operating decentralized combined 
heat and power plants. Risø & DTU - Department of Energy Engineering (ET). 
Denmark. Forskningscenter Risoe. Risoe-R, No. 1185(EN) - SEE PAGES 60 - 69
"""

import numpy as np
from math import log, pi, sqrt
import matplotlib.pyplot as plt
import PipeCatalogue

""" INPUT """
pipe='supply'       # [-]       pipe type (either 'supply' or 'return')
DN=20               # [mm]      nominal pipe diameter
IS=1                # [-]       pipe insulation series (poor - 1, 2, or 3 - good)
T_s=70              # [°C]      nominal supply temperature (assumed as constant)
T_r=40              # [°C]      nominal return temperature (assumed as constant)
T_gr=10             # [°C]      undisturbed ground temperature
lPipe=15            # [m]       pipe length
mFlow=0.01          # [kg/s]    water mass flow rate
T_init=40           # [°C]      initial water temperature
T_inlet=70          # [°C]      pipe inlet temperature

""" Numerical Parameters """
n_s=10                # [-]       number of nodes
delta_x=lPipe/(n_s-1) # [m]       spatial mesh size 
delta_t=1             # [s]       time step
n_t=10000             # [-]       number of time steps

""" Pipe Catalogue Data - LOGSTOR """
# Pre-insulated pipe layer diameters (water, steel, insulation, casing/mantle)

d_w,d_s,d_i,d_m=PipeCatalogue.LayerDiameters(DN,IS) # [m] 

d_g=d_m*1.5         # [m]       surrounding ground diameter (ASSUMPTION)

S_m=(d_m-d_i)/2     # [m]       casing thickness
S_d=1               # [m]       depth of pipes
S_c=0.15            # [m]       distance between supply and return

""" Water and Layer Properties """
# Water
rho_w=997           # [kg/m3]   density
cp_w=4.2*1000       # [J/kgK]   heat capacity

# Steel (P235TR1)
rho_s=7900          # [kg/m3]   density
cp_s=502.5          # [J/kgK]   heat capacity

# Insulation (PUR)
rho_i=30            # [kg/m3]   density
cp_i=133            # [J/kgK]   heat capacity
k_i=0.027           # [W/mK]    thermal conductivity

# Casing (Polyethylene HD)
rho_m=944           # [kg/m3]   density
cp_m=2250           # [J/kgK]   heat capacity
k_m=0.43            # [W7mK]    thermal conductivity

# Soil
rho_g=1400          # [kg/m3]   density
cp_g=1103           # [J/kgK]   heat capacity
k_g=1.6             # [W/mK]    thermal conductivity

""" Thermal Resistances """
# insulation
R_i=(1/(2*pi*k_i))*log(d_i/d_s)+(1/(2*pi*k_m))*log(d_m/d_i)
# soil
H=S_d+0.0685*k_g
R_g=(1/(2*pi*k_g))*log((4*H)/d_m)

""" Mutual Thermal Resistances """
# between water and insulation
R_wi=(1/(2*pi*k_i))*log((1+d_m/d_s)/2)

# between ground and surroundings
R_gu=(1/(2*pi*k_g))*log((4*H)/(d_m+d_g)+sqrt(((4*H)/(d_m+d_g))**2-1))

# between insulation and ground
R_ig=R_i+R_g-R_wi-R_gu

""" Scale Factor - Heat Loss """
# effect by two pipes underground
R_h=(1/(4*pi*k_g))*log(1+((2*H)/S_c)**2)

# correction factor theta
delta_Ts=T_s-T_gr
delta_Tr=T_r-T_gr

if pipe=='supply':
    gamma=delta_Tr/delta_Ts
elif pipe=='return':
    gamma=delta_Ts/delta_Tr

theta=(R_i+R_g)*((R_i+R_g-gamma*R_h)/((R_i+R_g)**2-R_h**2))

# heat transfer coefficients being scaled with a factor of theta
h_wi=delta_x*theta/R_wi     # water and insulation
h_gu=delta_x*theta/R_gu     # ground and surroundings
h_ig=delta_x*theta/R_ig     # insulation and ground

""" Heat Capacities """
# water and steel
C_ws=((delta_x*pi)/4)*(d_i**2*rho_w*cp_w+(d_s**2-d_i**2)*rho_s*cp_s)
# insulation
C_i=((delta_x*pi)/4)*((d_i**2-d_s**2)*rho_i*cp_i+(d_m**2-d_i**2)*rho_m*cp_m)
# ground (disturbed)
C_g=((delta_x*pi)/4)*((d_g**2-d_m**2)*rho_g*cp_g)

""" Numerical Constants """
# water 
Aw=mFlow*cp_w*delta_t/C_ws
Bw=h_wi*delta_t/C_ws
Cw=1+Bw

# ground
Ag=h_ig*delta_t/C_g
Bg=h_gu*delta_t/C_g
Cg=1+Ag+Bg;

# insulation
Ai=h_wi*delta_t/C_i
Bi=h_ig*delta_t/C_i
Ci=1+Ai-Ai*Bw/Cw+Bi-Bi*Ag/Cg

""" Initialize & Boundary """
# water
T_w=np.zeros((n_s,n_t+1))
T_w[:,0]=T_init
T_w[0,:]=T_inlet # Dirichlet boundary condition

# insulation
T_i=np.zeros((n_s,n_t+1))
T_i[:,0]=(T_init-1)

# ground (disturbed)
T_g=np.zeros((n_s,n_t+1))
T_g[:,0]=(T_gr+3)

""" Solution Algorithm """

for iT in range(1,n_t+1):
    
    # insulation
    for iS in range(1,n_s):
        T_i[iS,iT]=T_i[iS,iT-1]/Ci \
            +T_w[iS,iT-1]*(Ai*(1-Aw))/(Ci*Cw) \
            +T_w[iS-1,iT-1]*(Ai*Aw/(Ci*Cw)) \
            +T_g[iS,iT-1]*Bi/(Ci*Cg) \
            +T_gr*(Bi*Bg)/(Ci*Cg)
            
        T_i[0,iT]=T_i[1,iT] # Neumann boundary condition
    
    # water
    for iS in range(1,n_s):
        T_w[iS,iT]=T_w[iS,iT-1]*(1-Aw)/Cw \
            +T_w[iS-1,iT-1]*Aw/Cw \
            +T_i[iS,iT]*Bw/Cw
            
    # ground (disturbed)
    for iS in range(0,n_s):
        T_g[iS,iT]=T_g[iS,iT-1]/Cg \
            +T_i[iS,iT]*Ag/Cg \
            +T_gr*Bg/Cg
    
""" Plot - Pipe Outlet Temperature in Time """
t_plot=np.arange(n_t+1)*delta_t

plt.plot(t_plot,T_w[-1,:])
plt.xlabel('time [s]')
plt.ylabel('pipe outlet temperature [°C]')








