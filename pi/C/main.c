#include <stdio.h>

#include "SFMT/SFMT.h"

#define MONTE_CARLO 10000000

int main() {
	int insiders = 0;
	sfmt_t rng;

	sfmt_init_gen_rand(&rng, 0);

	for (int i = 0; i < MONTE_CARLO; i++) {
		double x = sfmt_genrand_res53(&rng),
		       y = sfmt_genrand_res53(&rng);
		if (x * x + y * y < 1)
			insiders++;
	}
	printf("PI = %f\n" , 4.0 * insiders / MONTE_CARLO);
}
