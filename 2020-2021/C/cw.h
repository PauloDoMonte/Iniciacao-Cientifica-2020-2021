#ifndef CW_H_INCLUDED
#define CW_H_INCLUDED

#define RAIO_TERRA 6378.1366
#define MI 398600.4418
#define PI 3.14159265359

float a(float w, int t);
float b(float w, int t);

// Funcoes de cw
float w(float altura);

float x0(float pitch, float yaw, float r0);
float Y0(float pitch, float yaw, float r0);
float z0(float pitch, float yaw, float r0);

float vx0(float x0, float vy0, int t, float w );
float vy0(float x0, float y0, int t, float w);
float vz0(float z0, int t, float w);

float xh(float x0, float vx0, float vy0, int t, float w);
float yh(float x0, float y0, float vx0, float vy0, int t, float w);
float zh(float z0, float vz0, int t, float w);

float vxh(float x0, float vx0, float vy0, int t, float w);
float vyh(float x0, float vx0, float vy0, int t, float w);
float vzh(float z0, float vz0, int t, float w);

// Funcoes de geracao de dados
int histograma_colisao(float alt, float r0, float rR, float pitch_inicial, float pitch_final, float yaw_inicial, float yaw_final, int t0, int tf);


#endif // CW_H_INCLUDED
