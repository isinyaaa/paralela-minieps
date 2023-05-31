CC=gcc
CFLAGS=-Wall -Wextra -Werror -pedantic -msse2 -DHAVE_SSE2 -DSFMT_MEXP=607
FILES=main.c SFMT/SFMT.c

all: build

build: $(FILES)
	$(CC) $(CFLAGS) -O3 -g $(FILES) -o main
