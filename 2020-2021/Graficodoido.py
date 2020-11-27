import random
import cw
import seaborn as se
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math as m

rodadasp = 181
rodadasy = 361


valores_p = np.linspace(-90,90,rodadasp)
valores_y = np.linspace(0,360,rodadasy)

N_simulacoes = rodadasp*rodadasy;

alt = 220

r0 = 3

t0 = 0
tf = 100

vx0 = 0
vy0 = 0
vz0 = 0

graf = 0
alfa = 0

x		= [0]*N_simulacoes
y		= [0]*N_simulacoes
z		= [0]*N_simulacoes
k		= [0]*N_simulacoes

z0 = 0
y0 = 0
x0 = 0

for pitch in valores_p:
	for yaw in valores_y:
		
		x0 = cw.x0(pitch,yaw,r0)
		y0 = cw.y0(pitch,yaw,r0)
		z0 = cw.z0(pitch,yaw,r0)

		
		r0 = m.sqrt(x0**2+y0**2+z0**2)

		data = cw.cinematica_cartesiano(alt,x0,y0,z0,r0,t0,tf,vx0,vy0,vz0,graf)
		x[alfa],y[alfa],z[alfa],k[alfa] = cw.volatilidade_k(data)
		alfa += 1
		
df = pd.DataFrame({'x':x,'y':y,'z':z,'k':k})
print(df)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.scatter(df['x'],df['y'],df['z'], c=df['k'])

ax.set_xlabel('Posição inicial relativa em x [km]')
ax.set_ylabel('Posição inicial relativa em y [km]')
ax.set_zlabel('Posição inicial relativa em z [km]')

plt.legend(loc = 'best')
fig.colorbar(surf,ax=ax)

plt.show()

