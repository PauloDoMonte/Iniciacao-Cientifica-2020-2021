import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
#from mpmath import mp

'''
cw.hist_nco(220,1,1e-2,0,90,-90,90,1,3000)
xh,yh,zh    ->  x(t) homogeneo,y(t) homogeneo,z(t) homogeneo, (Tempo de simulacao[s])
vxh,vyh,vzh ->  vxh(t) homogeneo,vyh(t) homogeneo,vzh(t) homogeneo, (Tempo de simulacao[s])
x0,y0,z0    ->  Posição iniciai para colisao [Grau,Km],(Tempo para colisao[s])
vx0,vy0,VZ0 ->  Velocidade inicial para colisao [km/s,km,s,(Tempo para colisao[s])]
w  ->  Velocidade angular em função da altitude
'''

# CONSTANTES
mi = 398600.4418
raio_terra = 6378.1366

# Termo utilizado nas equações de cw
def a(w,t):
	return(math.sin(w*t))
# Termo utilizado nas equações de cw
def b(w,t):
	return(math.cos(w*t))

def xp(x0,y0,z0,vx0,vy0,vz0,t,w,vex,vey,vez,chi,gamma):
	pass

def yp(x0,y0,z0,vx0,vy0,vz0,t,w,vex,vey,vez,chi,gamma):

	Sa,Sb,Sc = 0,0,0

	for n in range (1,150):

		Sa += ((math.pow(-1,n+1))/(n*pow(chi,n)))*((2*vex)/w + ((n*gamma*vey)/pow(w,2)))*(1/(1+pow(n*gamma/w,2)))
		Sb += ((math.pow(-1,n+1))/(n*pow(chi,n)))*(vey/w + ((2*n*gamma*vex)/pow(w,2)))*(1/(1+pow(n*gamma/w,2)))
		Sc += ((math.pow(-1,n+1))/(n*pow(chi,n)))*(vey + ((n*gamma*vey)/pow(w,2)))*(1/(1+pow(n*gamma/w,2)))*math.exp(-n*gamma*t)


	A = 2*vx0/w - 3*y0 + ((2*vex)/w)*math.log((chi + 1)/chi) - (Sa)
	B = vy0/w + (vey/w)*math.log((chi+1)/chi) + (Sb)
	D = 4*y0 - 2*vx0/w - ((2*vex)/w)*math.log((chi+1)/chi)
	#E = 6*w*y0 - 3*vx0 - 3*vex*math.log((chi+1)/chi)


	print(Sa)
	print(Sb)
	print(Sc)

	return(A*b(w,t)+B*a(w,t)+Sc+D)

def zp(x0,y0,z0,vx0,vy0,vz0,t,w,vex,vey,vez,chi,gamma):

	az = (vz0/w)+(vez/w)*math.log((chi+(1.0))/chi)

	sf = 0

	for n in range(1,150):
		p1 = math.pow(-1,n+1)
		p2 = math.pow(chi,n)
		k = 1/(1+(((n*gamma)*(n*gamma))/(w*w)))
		k1 = (n*gamma)/w
		k2 = w/(n*gamma)

		s1znt = ((p1)/(n*p2))*k*(a(w,t)+k1*(b(w,t)-((1.0)/math.exp(n*gamma*t))))

		sf = sf + s1znt

	return(z0*b(w,t)+az*a(w,t)-(vez/w)*sf)


# Calcula o x em função do t
def xh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( (vx0/w)*a(w,t)-((2.0)*vy0/w+(3.0)*x0)*b(w,t)+((2.0)*vy0/w+(4.0)*x0))

# Calcula o y em função do t
def yh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return(((4.0)*vy0/w+(6.0)*x0)*a(w,t)+((2.0)*vx0/w)*b(w,t)+(y0-(2.0)*vx0/w)-((3.0)*vy0+(6.0)*w*x0)*t)

# Calcula o z em função do t
def zh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return(z0*b(w,t)+(vz0/w)*a(w,t))

# Calcula o vx em função do t
def vxh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return ( vx0*b(w,t) + (2.*vy0+3.*w*x0)*a(w,t) )

# Calcula o vy em função do t
def vyh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( -2.*vx0*a(w,t) + (4.*vy0+6.*w*x0)*b(w,t) - (3.*vy0+6.*w*x0) )

# Calcula do vz em função do t
def vzh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( -z0*w*a(w,t) + vz0*b(w,t) )

# Calcula o x0
def x0(pitch,yaw,r0):
	return ( r0*math.sin((yaw*math.pi)/180)*math.sin((pitch*math.pi)/180) )

# Calcula o y0
def y0(pitch,yaw,r0):
	return( r0*math.sin((yaw*math.pi)/180)*math.cos((pitch*math.pi)/180) )

# Calcula o z0
def z0(pitch,yaw,r0):
	return ( r0*math.cos((yaw*math.pi)/180) )

# Calcula a velocidade inicial em z para ter um x final = 0
def vx0(x0,y0,z0,vy0,t,w):
	return ( -(w*x0*((4.0)-(3.0)*b(w,t))+(2.0)*((1.0)-b(w,t))*vy0)/(a(w,t)) )

# Calcula a velocidade inicial em z para ter um y final = 0
def vy0(x0,y0,z0,t,w):
	return (((((6.0)*x0*(w*t-a(w,t))-y0))*w*a(w,t))-((2.0)*w*x0*((4.0)-(3.0)*b(w,t))*((1.0)-b(w,t))))/(((4.0)*a(w,t)-(3.0)*w*t)*a(w,t)+(4.0)*((1.0)-b(w,t))*((1.0)-b(w,t)))

# Calcula a velocidade inicial em z para ter um z final = 0
def vz0(x0,y0,z0,vy0,t,w):
	return( -(z0*b(w,t)*w)/a(w,t) )

# Calcula a velocidade inicial em x para ter um x final = xr
def vx0_(xr,x0,vy0,t,w):
	return( (xr +  vy0*((2*b(w,t)-2)/w) + x0*(3*b(w,t)-4))*(w/a(w,t)) )

# Calcula a velocidade inicial em y para ter um y final = yr
def vy0_(xr,yr,x0,y0,t,w):
	
	A = 6*x0*a(w,t) - 6*w*x0*t
	B = ((4*a(w,t))/w) - 3*t
	C = ((w*xr)/a(w,t)) + ((3*w*x0*b(w,t))/a(w,t)) - ((4*w*x0)/a(w,t))
	numerador = ((-2*C*(b(w,t)-1))/w) -A + yr
	denominador = B + ((4*(b(w,t)-1)*(b(w,t)-1))/(w*a(w,t)))
	return(numerador/denominador)
	
# Calcula a velocidade inicial em z para ter um z final = zr
def vz0_(zr,z0,t,w):
	return( (zr*w)/a(w,t) - (z0*b(w,t)*w)/a(w,t) )

# Calcula o Omega da orbita
def w(altura):
	return( math.sqrt(mi/((raio_terra+altura)**3)) )

# Histograma de condições iniciais de colisão
def histograma_colisao(alt,r0,rR,pitch_inicial,pitch_final,yaw_inicial,yaw_final,t0,tf):
	w_ = w(220)
	hist=[0,0,0,0,0,0,0,0]
	v0_hist=['0-1','1-2.5','2.5-4','4-5.5','5.5-7.5','7.5-8.5','8.5-11','11-20']
	for pitch in range(pitch_inicial,pitch_final):
		print("Carregando: {}/{}".format(pitch,pitch_final))
		for yaw in range(yaw_inicial,yaw_final):
			x0_ = x0(pitch,yaw,r0)
			y0_ = y0(pitch,yaw,r0)
			z0_ = z0(pitch,yaw,r0)
			for tc in range(t0,tf):
				vy0_ = vy0(x0_,y0_,tc,w_)
				vx0_ = vx0(x0_,vy0_,tc,w_)
				vz0_ = vz0(z0_,tc,w_)
				k=0
				v0 = math.sqrt((vx0_*vx0_)+(vy0_*vy0_)+(vz0_*vz0_))
				for t in range(0,tc):
					xh_ = xh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
					yh_ = yh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
					zh_ = zh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
					rh = math.sqrt((xh_*xh_)+(yh_*yh_)+(zh_*zh_))
					if(rh/(alt+raio_terra) <= rR):	k+=1
					if(k>=tc-0.1):
						if((v0>0)and(v0<=1))		: hist[0]+=2
						elif((v0>1)and(v0<=2.5))	: hist[1]+=2
						elif((v0>2.5)and(v0<=4))	: hist[2]+=2
						elif((v0>4)and(v0<=5.5))	: hist[3]+=2
						elif((v0>5.5)and(v0<=7.5))	: hist[4]+=2
						elif((v0>7.5)and(v0<=8.5))	: hist[5]+=2
						elif((v0>8.5)and(v0<=11))	: hist[6]+=2
						elif((v0>11)and(v0<=20))	: hist[7]+=2
	dados = pd.DataFrame({"Data":hist,"V0":v0_hist})
	print(dados)

# Histograma de condições inicias de não colisão
def histograma_naocolisao(alt,r0,rR,pitch_inicial,pitch_final,yaw_inicial,yaw_final,t0,tf):
	w_ = w(alt)
	hist=[0,0]
	a=-1
	rf_histograma = [30,40]
	caminho = 'output_{}'.format(r0)
	arquivo = open(caminho, 'w') # Abre novamente o arquivo (escrita)
	arquivo.writelines('R0:{}\n'.format(r0))    # escreva o conteúdo criado anteriormente nele.
	arquivo.close()
	for rf in rf_histograma:
		a+=1
		for pitch in range(pitch_inicial,pitch_final):
			print('{}:\t{}\t{}\n'.format(rf,pitch,datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			arquivo = open(caminho, 'r') # Abra o arquivo (leitura)
			conteudo = arquivo.readlines()
			conteudo.append('{}:\t{}\t{}\n'.format(rf,pitch,datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))   # insira seu conteúdo
			arquivo = open(caminho, 'w') # Abre novamente o arquivo (escrita)
			arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
			arquivo.close()
			for yaw in range(yaw_inicial,yaw_final):
				x0_ = x0(pitch,yaw,r0)
				y0_ = y0(pitch,yaw,r0)
				z0_ = z0(pitch,yaw,r0)
				for tc in range(t0,tf):
					_vy0_ = vy0_(rf/math.sqrt(3),r0/math.sqrt(3),x0_,y0_,tc,w_)
					_vx0_ = vx0_(rf/math.sqrt(3),x0_,_vy0_,tc,w_)
					_vz0_ = vz0_(rf/math.sqrt(3),z0_,tc,w_)
					k,q=0,0
					for t in range(0,tc):
						xh_ = xh(x0_,y0_,z0_,_vx0_,_vy0_,_vz0_,t,w_)
						yh_ = yh(x0_,y0_,z0_,_vx0_,_vy0_,_vz0_,t,w_)
						zh_ = zh(x0_,y0_,z0_,_vx0_,_vy0_,_vz0_,t,w_)
						rh = math.sqrt((xh_*xh_)+(yh_*yh_)+(zh_*zh_))
						if(rh/(alt+raio_terra) <= rR):
							k+=1
							if(rh > 0):
								q+= 1
								if(k>=tc-0.1 and q>=tc-0.1):
									hist[a]+=4


		arquivo = open(caminho, 'r') # Abra o arquivo (leitura)
		conteudo = arquivo.readlines()
		conteudo.append('{}:{}\n'.format(rf,hist[a]))   # insira seu conteúdo
		arquivo = open(caminho, 'w') # Abre novamente o arquivo (escrita)
		arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
		arquivo.close()

# Gera banco de dados com a dinâmica relativa entre duas particulas utilizando pitch e yaw
def cinematica_esferica(alt,pitch,yaw,r0,t0,tf,vx0,vy0,vz0,graf):

	w_ = w(alt)

	x0_ = x0(pitch,yaw,r0)
	y0_ = y0(pitch,yaw,r0)
	z0_ = z0(pitch,yaw,r0)

	xt = np.zeros(tf - t0 + 1)
	yt = np.zeros(tf - t0 + 1)
	zt = np.zeros(tf - t0 + 1)

	vxt = np.zeros(tf - t0 + 1)
	vyt = np.zeros(tf - t0 + 1)

	vzt = np.zeros(tf - t0 + 1)

	tempo = np.zeros(tf - t0 + 1)

	r = np.zeros(tf - t0 + 1)
	v = np.zeros(tf - t0 + 1)

	for t in range (t0 , tf + 1):

		tempo[t] = t

		xt[t] = xh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		yt[t] = yh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		zt[t] = zh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)

		vxt[t] = vxh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		vyt[t] = vyh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		vzt[t] = vzh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)

		r[t] = math.sqrt(xt[t]**2+yt[t]**2+zt[t]**2)
		v[t] = math.sqrt(vxt[t]**2+vyt[t]**2+vzt[t]**2)

	Data = pd.DataFrame({'TEMPO': tempo, 'X[t]': xt, 'Y[t]': yt, 'Z[t]': zt, 'VXT': vxt, 'VYT': vyt, 'VZT': vzt, 'R[t]': r, 'V[t]': v})

	if(graf == 1):
		plt.figure(figsize = (8,6))

		plt.subplot(1,2,1)
		plt.plot(Data['TEMPO'],Data['R[t]'])
		plt.xlabel('Tempo [s]')
		plt.ylabel('Distância [km]')
		plt.title('Distância relativa em função do tempo [km]')
		plt.grid(True)

		plt.subplot(1,2,2)
		plt.plot(Data['TEMPO'],Data['V[t]'])
		plt.xlabel('Tempo [s]')
		plt.ylabel('Velocidade [km]')
		plt.title('Velocidade relativa em função do tempo [km/s]')
		plt.grid(True)

		plt.show()

	return(Data)

# Gera banco de dados com a dinâmica relativa colisional entre duas particulas
def cinematica_colisao(alt,pitch,yaw,r0,t0,tf,graf):

	w_ = w(alt)

	x0_ = x0(pitch,yaw,r0)
	y0_ = y0(pitch,yaw,r0)
	z0_ = z0(pitch,yaw,r0)

	t = tf

	vy0_ = vy0(x0_,y0_,z0_,t,w_)
	vx0_ = vx0(x0_,y0_,z0_,vy0_,t,w_)
	vz0_ = vz0(z0_,y0_,z0_,vy0_,t,w_)

	xt = np.zeros(tf - t0 + 1)
	yt = np.zeros(tf - t0 + 1)
	zt = np.zeros(tf - t0 + 1)

	vxt = np.zeros(tf - t0 + 1)
	vyt = np.zeros(tf - t0 + 1)

	vzt = np.zeros(tf - t0 + 1)

	tempo = np.zeros(tf - t0 + 1)

	r = np.zeros(tf - t0 + 1)
	v = np.zeros(tf - t0 + 1)

	for t in range (t0 , tf + 1):

		tempo[t] = t

		xt[t] = xh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
		yt[t] = yh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
		zt[t] = zh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)

		vxt[t] = vxh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
		vyt[t] = vyh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
		vzt[t] = vzh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)

		r[t] = math.sqrt(xt[t]**2+yt[t]**2+zt[t]**2)
		v[t] = math.sqrt(vxt[t]**2+vyt[t]**2+vzt[t]**2)

	Data = pd.DataFrame({'TEMPO': tempo, 'X[t]': xt, 'Y[t]': yt, 'Z[t]': zt, 'VXT': vxt, 'VYT': vyt, 'VZT': vzt, 'R[t]': r, 'V[t]': v})

	if(graf == 1):
		plt.figure(figsize = (8,6))

		plt.subplot(1,2,1)
		plt.plot(Data['TEMPO'],Data['R[t]'])
		plt.xlabel('Tempo [s]')
		plt.ylabel('Distância [km]')
		plt.title('Distância relativa em função do tempo [km]')
		plt.grid(True)

		plt.subplot(1,2,2)
		plt.plot(Data['TEMPO'],Data['V[t]'])
		plt.xlabel('Tempo [s]')
		plt.ylabel('Velocidade [km]')
		plt.title('Velocidade relativa em função do tempo [km/s]')
		plt.grid(True)

		plt.show()

	return(Data)

# Calcular a estabilidade de uma dinâmica relativa utilizando o termo K
def volatilidade_k(dataframe):

	tamanho = len(dataframe)
	alfa = 0

	b = 0
	k = 0

	for i in range(1,tamanho-1):
		alfa = alfa + abs(dataframe['R[t]'][i+1] - dataframe['R[t]'][i])

	k = pow(alfa/tamanho,1/2)

	return(dataframe['X[t]'][0],dataframe['Y[t]'][0],dataframe['Z[t]'][0],k)

# Gera banco de dados com a dinâmica relativa entre duas particulas utilizando x0, y0, z0
def cinematica_cartesiano(alt,x0,y0,z0,r0,t0,tf,vx0,vy0,vz0,graf):

	w_ = w(alt)

	x0_ = x0
	y0_ = y0
	z0_ = z0

	xt = np.zeros(tf - t0 + 1)
	yt = np.zeros(tf - t0 + 1)
	zt = np.zeros(tf - t0 + 1)

	vxt = np.zeros(tf - t0 + 1)
	vyt = np.zeros(tf - t0 + 1)

	vzt = np.zeros(tf - t0 + 1)

	tempo = np.zeros(tf - t0 + 1)

	r = np.zeros(tf - t0 + 1)
	v = np.zeros(tf - t0 + 1)

	for t in range (t0 , tf + 1):

		tempo[t] = t

		xt[t] = xh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		yt[t] = yh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		zt[t] = zh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)

		vxt[t] = vxh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		vyt[t] = vyh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)
		vzt[t] = vzh(x0_,y0_,z0_,vx0,vy0,vz0,t,w_)

		r[t] = math.sqrt(xt[t]**2+yt[t]**2+zt[t]**2)
		v[t] = math.sqrt(vxt[t]**2+vyt[t]**2+vzt[t]**2)

	Data = pd.DataFrame({'TEMPO': tempo, 'X[t]': xt, 'Y[t]': yt, 'Z[t]': zt, 'VXT': vxt, 'VYT': vyt, 'VZT': vzt, 'R[t]': r, 'V[t]': v})

	if(graf == 1):
		plt.figure(figsize = (8,6))

		plt.subplot(1,2,1)
		plt.plot(Data['TEMPO'],Data['R[t]'])
		plt.xlabel('Tempo [s]')
		plt.ylabel('Distância [km]')
		plt.title('Distância relativa em função do tempo [km]')
		plt.grid(True)

		plt.subplot(1,2,2)
		plt.plot(Data['TEMPO'],Data['R[t]'])
		plt.xlabel('Tempo [s]')
		plt.ylabel('Velocidade [km]')
		plt.title('Velocidade relativa em função do tempo [km/s]')
		plt.grid(True)

		plt.show()

	return(Data)


def hist_relacionado(alt,r0):

	hist = np.zeros(11)
	v0_ = np.linspace(-40,40,4000)
	
	for pitch in range(-90,90):
		for yaw in range(0,360):
			
			print("Carregando Pitch {} Yaw {}".format(pitch,yaw))
			
			print(hist)
			
			for v0 in v0_:
				
				vx0_ = v0/math.sqrt(3)
				vy0_ = v0/math.sqrt(3)
				vz0_ = v0/math.sqrt(3)
	
				Data = cinematica_esferica(alt,pitch,yaw,3,0,3000,vx0_,vy0_,vz0_,0)
				
				k = 0
				
				for t in range (0,2999):
					
					if (Data['R[t]'][t] <= 100): k += 1
				
				if (k >= 2998):
					if((Data['R[t]'][2999]==0)): hist[0]+=1
					elif((Data['R[t]'][2999]>0)and(Data['R[t]'][2999]<=10)): hist[1]+=1
					elif((Data['R[t]'][2999]>10)and(Data['R[t]'][2999]<=20)): hist[2]+=1
					elif((Data['R[t]'][2999]>20)and(Data['R[t]'][2999]<=30)): hist[3]+=1
					elif((Data['R[t]'][2999]>30)and(Data['R[t]'][2999]<=40)): hist[4]+=1
					elif((Data['R[t]'][2999]>40)and(Data['R[t]'][2999]<=50)): hist[5]+=1
					elif((Data['R[t]'][2999]>50)and(Data['R[t]'][2999]<=60)): hist[6]+=1
					elif((Data['R[t]'][2999]>60)and(Data['R[t]'][2999]<=70)): hist[7]+=1
					elif((Data['R[t]'][2999]>70)and(Data['R[t]'][2999]<=80)): hist[8]+=1
					elif((Data['R[t]'][2999]>80)and(Data['R[t]'][2999]<=90)): hist[9]+=1
					elif((Data['R[t]'][2999]>90)and(Data['R[t]'][2999]<=100)): hist[10]+=1
					
#cw.hist_relacionado(220,3,-90,90,0,360,-2,2)

