CC=gcc
CCFLAGS=-Wall -O0
LDFLAGS=-lm -lpthread
IF ?= 0
IF_STR = $(shell if [ $(IF) -gt 0 ]; then for i in `seq 1 $(IF)`; do echo 'IF_GT_MAX '; done; fi)
BIN=contention
SRC=main.c

all:
	sed "s!//@#@IF!$(IF_STR)!" $(SRC) > .$(SRC)
	$(CC) $(CCFLAGS) .$(SRC) -o $(BIN) $(LDFLAGS)
	rm -f .$(SRC)

.PHONY: clean
clean:
	rm -f contention
