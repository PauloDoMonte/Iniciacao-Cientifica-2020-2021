#!/bin/bash

gcc -c cw.c -o cw.o
gcc -c main.c -o main.o
gcc cw.o main.o -o main -lm
./main
