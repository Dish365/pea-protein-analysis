use rand::distributions::{Distribution, Normal};
use rayon::prelude::*;

#[no_mangle]
pub extern "C" fn run_economic_monte_carlo(
    base_values: *const f64,
    len: usize,
    iterations: usize,
    uncertainty: f64,
    results: *mut f64
) {
    let values = unsafe { std::slice::from_raw_parts(base_values, len) };
    let mut simulated_npvs = Vec::with_capacity(iterations);
    
    // Parallel simulation using rayon
    simulated_npvs.par_extend(
        (0..iterations).into_par_iter().map(|_| {
            let normal = Normal::new(0.0, uncertainty).unwrap();
            let mut rng = rand::thread_rng();
            
            // Calculate NPV with random variations
            values.iter().enumerate().map(|(i, &value)| {
                let variation = normal.sample(&mut rng);
                value * (1.0 + variation) / (1.1f64.powi(i as i32))
            }).sum()
        })
    );
    
    // Calculate statistics
    let mean = simulated_npvs.par_iter().sum::<f64>() / iterations as f64;
    let variance = simulated_npvs.par_iter()
        .map(|&x| (x - mean).powi(2))
        .sum::<f64>() / iterations as f64;
    let std_dev = variance.sqrt();
    
    unsafe {
        *results.offset(0) = mean;
        *results.offset(1) = std_dev;
        *results.offset(2) = simulated_npvs.iter().copied().fold(f64::INFINITY, f64::min);
        *results.offset(3) = simulated_npvs.iter().copied().fold(f64::NEG_INFINITY, f64::max);
    }
} 