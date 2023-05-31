use rand::prelude::*;
use rand_pcg::Pcg64Mcg;


fn main() {
    let mut rng = Pcg64Mcg::from_entropy();
    let monte_carlo = 10_000_000;
    let mut inside = 0;

    for _ in 0..monte_carlo {
        let x = rng.gen_range(0.0..1.0);
        let y = rng.gen_range(0.0..1.0);

        if x * x + y * y <= 1.0 {
            inside += 1;
        }
    }
    print!("pi = {}\n", 4.0 * inside as f64 / monte_carlo as f64);
}
