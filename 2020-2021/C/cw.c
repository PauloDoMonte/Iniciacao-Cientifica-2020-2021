#include "cw.h"
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>

float a(float w, int t){
  return(sin(w*t));
}

float b(float w, int t){
  return(cos(w*t));
}

float w(float altura){
  return(sqrt(MI/(pow(RAIO_TERRA+altura,3))));
}

float x0(float pitch, float yaw, float r0){
  return ( r0*sin((yaw*PI)/180)*sin((pitch*PI)/180) );
}

float Y0(float pitch, float yaw, float r0){
  return( r0*sin((yaw*PI)/180)*cos((pitch*PI)/180) );
}

float z0(float pitch, float yaw, float r0){
  return ( r0*cos((yaw*PI)/180) );
}

float vx0(float x0, float vy0, int t, float w ){
  return ( -(w*x0*((4.0)-(3.0)*b(w,t))+(2.0)*((1.0)-b(w,t))*vy0)/(a(w,t)) );
}

float vy0(float x0, float y0, int t, float w){
  return (((((6.0)*x0*(w*t-a(w,t))-y0))*w*a(w,t))-((2.0)*w*x0*((4.0)-(3.0)*b(w,t))*((1.0)-b(w,t))))/(((4.0)*a(w,t)-(3.0)*w*t)*a(w,t)+(4.0)*((1.0)-b(w,t))*((1.0)-b(w,t)));
}

float vz0(float z0, int t, float w){
  return( -(z0*b(w,t)*w)/a(w,t) );
}

float xh(float x0, float vx0, float vy0, int t, float w){
  return( (vx0/w)*a(w,t)-((2.0)*vy0/w+(3.0)*x0)*b(w,t)+((2.0)*vy0/w+(4.0)*x0));
}

float yh(float x0, float y0, float vx0, float vy0, int t, float w){
  return(((4.0)*vy0/w+(6.0)*x0)*a(w,t)+((2.0)*vx0/w)*b(w,t)+(y0-(2.0)*vx0/w)-((3.0)*vy0+(6.0)*w*x0)*t);
}

float zh(float z0, float vz0, int t, float w){
  return(z0*b(w,t)+(vz0/w)*a(w,t));
}

float vxh(float x0, float vx0, float vy0, int t, float w){
  return ( vx0*b(w,t) + (2.*vy0+3.*w*x0)*a(w,t) );
}
float vyh(float x0, float vx0, float vy0, int t, float w){
  return( -2.*vx0*a(w,t) + (4.*vy0+6.*w*x0)*b(w,t) - (3.*vy0+6.*w*x0) );
}
float vzh(float z0, float vz0, int t, float w){
  return( -z0*w*a(w,t) + vz0*b(w,t) );
}

int histograma_colisao(float altura, float r0, float rR, float pitch_inicial, float pitch_final, float yaw_inicial, float yaw_final, int t0, int tf){
  // Declaracao de variaveis locais
    float pitch = 0,yaw = 0,tc = 0,t = 0,rh = 0;
    float x0_ = 0,y0_ = 0,z0_ = 0,vx0_ = 0,vy0_ = 0,vz0_ = 0,xh_ = 0,yh_ = 0,zh_ = 0,w_ = 0;
    float v0 = 0,k = 0;
    int hist[8] = {0,0,0,0,0,0,0,0};
    w_ = w(altura);

    for(pitch = pitch_inicial; pitch <= pitch_final; pitch++){
        for(yaw = yaw_inicial; yaw <= yaw_final; yaw++){
            x0_ = x0(pitch,yaw,r0);
            y0_ = Y0(pitch,yaw,r0);
            z0_ = z0(pitch,yaw,r0);
            for(tc = t0; tc <= tf; tc++){
                vy0_ = vy0(x0_,y0_,tc,w_);
                vx0_ = vx0(x0_,vy0_,tc,w_);
                vz0_ = vz0(z0_,tc,w_);
                v0 = sqrt((vx0_*vx0_)+(vy0_*vy0_)+(vz0_*vz0_));
                k=0;
                for(t = 0; t <= tc; t++){
                    xh_ = xh(x0_,vx0_,vy0_,t,w_);
                    yh_ = yh(x0_,y0_,vx0_,vy0_,t,w_);
                    zh_ = zh(z0_,vz0_,t,w_);
                    rh = sqrt((xh_*xh_)+(yh_*yh_)+(zh_*zh_));
                    if(rh/(altura+RAIO_TERRA) <= rR){k++;}
                    if(k>=(tc-0.1)){
                        if((v0>0)&&(v0<=1)){hist[0]+=1;}
                        if((v0>1)&&(v0<=2.5)){hist[1]+=1;}
                        if((v0>2.5)&&(v0<=4)){hist[2]+=1;}
                        if((v0>4)&&(v0<=5.5)){hist[3]+=1;}
                        if((v0>5.5)&&(v0<=7.5)){hist[4]+=1;}
                        if((v0>7.5)&&(v0<=8.5)){hist[5]+=1;}
                        if((v0>8.5)&&(v0<=11)){hist[6]+=1;}
                        if((v0>11)&&(v0<=20)){hist[7]+=1;}
                    }
                }
            }
        }
        printf("%f\n", pitch);
    }

    FILE *file;
    file = fopen("Histograma_colisao.csv","w");
    fprintf(file, "V0,Dados\n0-1,%i\n1-2.5,%i\n2.5-4,%i\n4-5.5,%i\n5.5-7.5,%i\n7.5-8.5,%i\n8.5-11,%i\n11-20,%i\n", hist[0],hist[1],hist[2],hist[3],hist[4],hist[5],hist[6],hist[7]);

}
