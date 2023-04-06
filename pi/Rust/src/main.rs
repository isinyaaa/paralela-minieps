use rand::Rng;

fn main() {
    let mut rng = rand::thread_rng();
    let monte_carlo = 10_000_000;

    let mut inside = 0;

    for _ in 0..monte_carlo {
        let x = rng.gen::<f64>();
        let y = rng.gen::<f64>();

        if x * x + y * y <= 1.0 {
            inside += 1;
        }
    }
    print!("pi = {}\n", 4.0 * inside as f64 / monte_carlo as f64);
}
