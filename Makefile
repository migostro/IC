CFLAGS = -Wall -pedantic
CC = g++
RM = rm

fluxo: fluxo.cpp node.h node.cpp 
	$(CC) $(CFLAGS) fluxo.cpp node.cpp -o fluxo

clean: 
	$(RM) *.o *~
