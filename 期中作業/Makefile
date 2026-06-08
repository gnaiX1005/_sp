CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lutil

all: telnetd

telnetd: telnetd.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f telnetd

run: telnetd
	./telnetd

.PHONY: all clean run
