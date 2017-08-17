#Just a simple makefile to compile all Thread related exercises
CC = g++
CFLAGS  = -g -Wall -std=c++11 
CLIBS = -pthread

all: prodcons threads1

# Compile ProdCons
prodcons:  ProdCons.o 
	$(CC) $(CFLAGS) $(CLIBS) -o ProdCons ProdCons.o

# Compile Threads1
threads1: Threads1.o
	$(CC) $(CFLAGS) $(CLIBS) -o Threads1 Threads1.o

#
ProdCons.o:  ProdCons.cpp 
	$(CC) $(CFLAGS) -c ProdCons.cpp

#
Threads1.o:  Threads1.cpp 
	$(CC) $(CFLAGS) -c Threads1.cpp


# Clean all images and object files!
#
clean: 
	$(RM) ProdCons Threads1 *.o *~
