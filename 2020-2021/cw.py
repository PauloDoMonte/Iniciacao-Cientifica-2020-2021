import math,pandas
'''
xh,yh,zh    ->  x(t) homogeneo,y(t) homogeneo,z(t) homogeneo, (Tempo de simulacao[s])
vxh,vyh,vzh ->  vxh(t) homogeneo,vyh(t) homogeneo,vzh(t) homogeneo, (Tempo de simulacao[s])
x0,y0,z0    ->  Posição iniciai para colisao [Grau,Km],(Tempo para colisao[s])
vx0,vy0,VZ0 ->  Velocidade inicial para colisao [km/s,km,s,(Tempo para colisao[s])]
w  ->  Velocidade angular em função da altitude
'''

# CONSTANTES
mi = 398600.4418
raio_terra = 6378.1366

def a(w,t):
	return(math.sin(w*t))

def b(w,t):
	return(math.cos(w*t))

def xh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( ((vx0/w)*a(w,t)) - ((2.)*vy0/w+(3.)*x0)*b(w,t) + ((2.)*vy0/w+(4.)*x0) )

def yh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( ((2.)*vx0/w)*b(w,t) + ((4.)*vy0/w+(6.)*x0)*a(w,t) + (y0-(2.)*vx0/w) - ((3.)*vy0+(6.)*w*x0)*t )

def zh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( z0*b(w,t) + (vz0/w)*a(w,t) )

def vxh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return ( vx0*b(w,t) + (2.*vy0+3.*w*x0)*a(w,t) )

def vyh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( -2.*vx0*a(w,t) + (4.*vy0+6.*w*x0)*b(w,t) - (3.*vy0+6.*w*x0) )

def vzh(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( -z0*w*a(w,t) + vz0*b(w,t) )

def x0(pitch,yaw,r0):
	return ( r0*math.sin((yaw*math.pi)/180)*math.sin((pitch*math.pi)/180) )

def y0(pitch,yaw,r0):
	return( r0*math.sin((yaw*math.pi)/180)*math.cos((pitch*math.pi)/180) )

def z0(pitch,yaw,r0):
	return ( r0*math.cos((yaw*math.pi)/180) )

def vx0(x0,y0,z0,vx0,vy0,vz0,t,w):
	return ( -(w*x0*((4.0)-(3.0)*b(w,t))+(2.0)*((1.0)-b(w,t))*vy0)/(a(w,t)) )

def vy0(x0,y0,z0,vx0,vy0,vz0,t,w):
	return ( (((((6.0)*x0*(w*t-a(w,t))-y0))*w*a(w,t))-((2.0)*w*x0*((4.0)-(3.0)*b(w,t))*((1.0)-b(w,t))))/(((4.0)*a(w,t)-(3.0)*w*t)*a(w,t)+(4.0)*((1.0)-b(w,t))*((1.0)-b(w,t))) )

def vz0(x0,y0,z0,vx0,vy0,vz0,t,w):
	return( -(z0*b(w,t)*w)/a(w,t) )

def w(altura):
	return( math.sqrt(mi/((raio_terra+altura)**3)) )

# Simulações
def hist_ci(alt,r0,rR,pitch_inicial,pitch_final,yaw_inicial,yaw_final,t0,tf):
	w_ = w(220)
	hist=[0,0,0,0,0,0,0,0]
	v0_hist=['0-1','1-2.5','2.5-4','4-5.5','5.5-7.5','7.5-8.5','8.5-11','11-20']
	for pitch in range(pitch_inicial,pitch_final):
		print("Carregando: {}/{}".format(pitch,pitch_final))
		for yaw in range(yaw_inicial,yaw_final):
			x0_ = x0(pitch,yaw,r0)
			y0_ = x0(pitch,yaw,r0)
			z0_ = x0(pitch,yaw,r0)
			for tc in range(t0,tf):
				vy0_ = vy0(x0_,y0_,z0_,0,0,0,tc,w_)
				vx0_ = vx0(x0_,y0_,z0_,0,vy0_,0,tc,w_)
				vz0_ = vz0(x0_,y0_,z0_,0,0,0,tc,w_)
				k=0
				v0 = math.sqrt((vx0_*vx0_)+(vy0_*vy0_)+(vz0_*vz0_))
				for t in range(0,tc):
					xh_ = xh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
					yh_ = yh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
					zh_ = xh(x0_,y0_,z0_,vx0_,vy0_,vz0_,t,w_)
					rh = math.sqrt((xh_*xh_)+(yh_*yh_)+(zh_*zh_))
					if(rh/(alt+raio_terra) < rR):	k+=1
					if(k>=tc-0.1):
						if((v0>0)and(v0<=1))		: hist[0]+=2
						elif((v0>1)and(v0<=2.5))	: hist[1]+=2
						elif((v0>2.5)and(v0<=4))	: hist[2]+=2
						elif((v0>4)and(v0<=5.5))	: hist[3]+=2
						elif((v0>5.5)and(v0<=7.5))	: hist[4]+=2
						elif((v0>7.5)and(v0<=8.5))	: hist[5]+=2
						elif((v0>8.5)and(v0<=11))	: hist[6]+=2
						elif((v0>11)and(v0<=20))	: hist[7]+=2
	dados = pandas.DataFrame({"Data":hist,"V0":v0_hist})
	print(dados)
