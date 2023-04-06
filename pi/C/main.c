#include <stdlib.h>
#include <stdio.h>

#define MONTE_CARLO 10000000

int main() {
	int insiders = 0;
	for (int i = 0; i < MONTE_CARLO; i++) {
		double x = (double)rand() / RAND_MAX;
		double y = (double)rand() / RAND_MAX;
		if (x * x + y * y <= 1.0)
			insiders++;
	}
	printf("PI = %f\n" , 4.0 * insiders / MONTE_CARLO);
}
