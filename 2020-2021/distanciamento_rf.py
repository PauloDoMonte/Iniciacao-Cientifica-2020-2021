import cw,math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as se

w = cw.w(220)
altura = 220
t0 = 0
tf = 3000
r0 = 3
graf = 0

pi,pf = -90,90#-90,90
yi,yf = 0,360#0,360
pitch_v,yaw_v = np.linspace(pi,pf,(pf-pi)),np.linspace(yi,yf,(yf-yi))
oscilacao = np.zeros((pf-pi)*(yf-yi))
i=0
dt = pd.DataFrame({'Index':oscilacao,'Pitch':oscilacao,'Yaw':oscilacao,'Oscilação':oscilacao,'Vx0':oscilacao,'Y0':oscilacao,'Condicao':oscilacao})

for pitch in pitch_v:
	for yaw in yaw_v:
		x0 = cw.x0(pitch,yaw,r0)
		y0 = cw.y0(pitch,yaw,r0)
		z0 = cw.z0(pitch,yaw,r0)
		vx0 = y0/(2*w)
		vy0 = 0
		vz0 = 0
		data = cw.cinematica_esferica(altura,pitch,yaw,r0,t0,tf,vx0,vy0,vz0,graf)
		max = np.max(data["R[t]"])
		min = np.min(data["R[t]"])
		oscilacao[i] = data["R[t]"][2999]
		dt['Pitch'][i] = round(pitch,2)
		dt['Yaw'][i] = round(yaw,2)
		dt['Oscilação'][i] = oscilacao[i]
		dt['Vx0'][i] = vx0
		dt['Y0'][i] = y0
		dt['Index'][i] = i
		i+=1
	print(pitch)

cont = 0
for i in range(0,len(dt['Yaw'])):
	if(dt['Oscilação'][i] <= 100):
		cont += 1

yaw_,pitch_,rf_ = np.zeros(cont),np.zeros(cont),np.zeros(cont)
i_ = 0

for i in range(0,len(dt['Yaw'])):
	if(dt['Oscilação'][i] <= 100):
		yaw_[i_] = dt['Yaw'][i]
		pitch_[i_] = dt['Pitch'][i]
		rf_[i_] = dt['Oscilação'][i]
		i_ += 1

df = pd.DataFrame({'Pitch':pitch_,'Yaw':yaw_,'Rf':rf_})
df_new = df.pivot(index='Pitch',columns='Yaw',values='Rf')
df_new.to_csv('distanciamento.csv', sep=",")
se.heatmap(df_new)
plt.title("Mapa do R final relativo em função dos pares de ângulos")
plt.show()

'''
dt_new = dt.pivot(index='Pitch',columns='Yaw',values='Oscilação')
dt_new.to_csv('distanciamento.csv', sep=",")
se.heatmap(dt_new)
plt.title("Mapa de oscilação da distância relativa em função dos pares de ângulos")
plt.show()
'''
