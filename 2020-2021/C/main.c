#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "cw.h"

int main()
{
    float x0_,y0_,z0_;
    float vx0_,vy0_,vz0_;
    float xh_,yh_,zh_;
    float rf;

    int t = 1;
    float pitch = 30, yaw = 50, r0 = 3;
    float w_ = w(220);

    int cont = 0;

  for(yaw = 0;yaw < 360;yaw++)        {
    for(pitch = -90;pitch<=90;pitch++)  {
      for(t=1;t<=3000;t++)                {

          x0_ = x0(pitch,yaw,r0);
          y0_ = Y0(pitch,yaw,r0);
          z0_ = z0(pitch,yaw,r0);

          vy0_ = vy0(x0_,y0_,t,w_);
          vx0_ = vx0(x0_,vy0_,t,w_);
          vz0_ = vz0(z0_,t,w_);

          xh_ = xh(x0_,vx0_,vy0_,t,w_);
          yh_ = yh(x0_,y0_,vx0_,vy0_,t,w_);
          zh_ = zh(z0_,vz0_,t,w_);

          rf = sqrt((xh_*xh_)+(yh_*yh_)+(zh_*zh_));
          /*printf("Vx0:%f\nVy0:%f\nVz0:%f\n", vx0_,vy0_,vz0_);
          printf("\nX:%f\nY:%f\nZ:%f\n", xh_,yh_,zh_);
          printf("\nX0:%f\nY0:%f\nZ0:%f\n", x0_,y0_,z0_);*/

          if(rf > 0.0001) cont++;
          printf("Erros graves = %i\n",cont);

      }
    }
  }
}
