# Use the gcc compiler
CC=gcc

CFLAGS= -Wall

all: iopi

iopi: ./src/main.o ./src/abe_iopi.o ./src/help.o
	$(CC) ./src/main.o ./src/help.o ./src/abe_iopi.o -o iopi

main.o: ./src/main.c
	$(CC) $(CFLAGS) ./src/main.c
    
abe_iopi.o: ./src/abe_iopi.c
	$(CC) $(CFLAGS) ./src/abe_iopi.c
	
help.o: ./src/help.c
	$(CC) $(CFLAGS) ./src/help.c
    
clean:
	rm *o iopi