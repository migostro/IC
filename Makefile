CFLAGS = -Wall -pedantic
CC = g++
RM = rm

fluxo: fluxo.cpp node.h node.cpp 
	$(CC) $(CFLAGS) fluxo.cpp node.cpp -o fluxo
#fluxo: fluxo.o
#	$(CC) $(CFLAGS) fluxo.o -o fluxo
#
#fluxo.o: node.o fluxo.cpp 
#	$(CC) $(CFLAGS) node.o fluxo.cpp  -o fluxo
#
#node.o: node.h node.cpp 
#	$(CC) $(CFLAGS) node.cpp -o node.o

clean: 
	$(RM) *.o *~
