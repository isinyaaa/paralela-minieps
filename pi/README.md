# PI Approximation Algorithm

This is an approximation to the PI constant using a Monte Carlo simulation.

## Implementation

It follows the logic from the pseudocode below:

```py
ITERATIONS = 1e10^7

inside = 0

for i in 0..ITERATIONS:
    x = random()
    y = random()
    # check if we're inside the unit circle
    if (x^2 + y^2 <= 1):
        inside = inside + 1

# We know that the ratio of circle_area/total_area = (pi * r^2)/((2 * r)^2),
# where r is the radius of a circle tangent to a square of side length 2 * r.
# Thus, for whatever r it follows that pi = 4 * circle_area/total_area.
# Note that as 0 <= random() < 1 (as usually follows) we are only analyzing the
# area of a single quadrant, but that is not a problem as dividing both the
# circle_area and total_area by 4 yields the same result.
pi = 4.0 * inside / ITERATIONS
```

This pseudocode was implemented using the C and Rust languages.

### C

SIMD-oriented Fast Mersenne Twister (`SFMT`) is used for maximum performance.

### Rust

The `rand_pcg` crate is used for simplicity. It employs the `PCG64` as its
pseudo-number generator, which has been recognized for its performance.

## Performance analysis

The analysis was initially done using the `perf` tool to measure run times.
Then both versions instruction counts were analyzed using `callgrind` together
with `kcachegrind` (for visualization).

Using `callgrind` we could see that calls to the PRNG were the most expensive
operations in both versions.
In order to optimize the C version, we used `SFMT` which is a SIMD-oriented
implementation of the Mersenne Twister PRNG. This resulted in a ~3x speedup.
For the Rust version we opted for the more commonly known `PCG64` PRNG, which
resulted in a ~3x speedup as well.

We wanted to use `PCG64` in the C version as well, but we couldn't find a
suitable implementation.

## Changelog

### 0.2

- C: now uses `SFMT`.
- Rust: now uses `rand_pcg`.

### 0.1

- C and Rust versions were implemented using random functions from their
  respective standard libraries (no effort was made to optimize either)
