import cw,math

w = cw.w(220)
for t in range(1,3000):
	#t = 30
	

	df = 3

	rr = df/math.sqrt(3)

	x0 = cw.x0(0,0,3)
	y0 = cw.y0(0,0,3)
	z0 = cw.z0(0,0,3)

	vy0 = cw.vy0_(rr,rr,x0,y0,t,w)
	vx0 = cw.vx0_(rr,x0,vy0,t,w)
	vz0 = cw.vz0_(rr,z0,t,w)

	xh = cw.xh(x0,y0,z0,vx0,vy0,vz0,t,w)
	yh = (cw.yh(x0,y0,z0,vx0,vy0,vz0,t,w))
	zh = cw.zh(x0,y0,z0,vx0,vy0,vz0,t,w)
	r = (math.sqrt((xh*xh)+(yh*yh)+(zh*zh)))



	print("""Velocidades para o Rf = {}
	VX0:  {}
	VY0:  {}
	VZ0:  {}

	xh:   {}
	yh:   {}
	zh:   {}

	""".format(rr*math.sqrt(3),vx0,vy0,vz0,xh,yh,zh))

	
	print(r)
