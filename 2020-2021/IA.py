import cw,random

var,i=[0,0,0,0,0],0
c4a = 10
while(c4a >= 0.0001):
	
	pitch_,yaw_,vx0_,vy0_,vz0_=var[0],var[1],var[2],var[3],var[4]
	c1,c2,c3,c4,c5,c6,c7 = cw.volatilidade_k(cw.cinematica_esferica(220,pitch_,yaw_,3,0,3000,vx0_,vy0_,vz0_,0))
	
	
	if (i == 0):a,b = -90,90
	if (i == 1):a,b =  0,360
	if (i > 1):a,b  = -0.01,0.01
		
	var[i] = random.uniform(a,b)
	
	i+=1
	if(i == 5):i = 0
	
	if(c4 < c4a):c1a,c2a,c3a,c4a,c5a,c6a,c7a = c1,c2,c3,c4,c5,c6,c7

	
	
	
	
	print("x0a = {}\t\ty0a = {}\t\tz0a = {}\t\tka = {}\t\tvx0a = {}\t\tvy0a = {}\t\tvz0a = {}".format(c1a,c2a,c3a,c4a,c5a,c6a,c7a))
	print("x0 = {}\t\ty0 = {}\t\tz0 = {}\t\tk = {}\t\tvx0 = {}\t\tvy0 = {}\t\tvz0 = {}".format(c1,c2,c3,c4,c5,c6,c7))
	
cw.cinematica_cartesiano(220,c1a,c2a,c3a,3,0,3000,c5a,c6a,c7a,1)