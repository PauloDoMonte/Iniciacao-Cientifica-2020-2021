import cw,math

altura = 220
r0 = 1
t0,tf = 0,3000
graf = 1
pitch,yaw = 0,0
vx0,vy0,vz0 = 3/math.sqrt(3),3/math.sqrt(3),3/math.sqrt(3)
cw.cinematica_esferica(altura,pitch,yaw,r0,t0,tf,vx0,vy0,vz0,graf)
cw.cinematica_esferica(altura,pitch,yaw,20,t0,tf,vx0,vy0,vz0,graf)
