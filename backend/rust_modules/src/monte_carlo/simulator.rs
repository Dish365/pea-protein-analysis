use std::ffi::c_double;
use rayon::prelude::*;

#[no_mangle]
pub extern "C" fn run_monte_carlo_simulation(
    base_values: *const c_double,
    len: usize,
    iterations: usize,
    uncertainty: c_double,
    results: *mut c_double
) {
    let values = unsafe { std::slice::from_raw_parts(base_values, len) };
    let mut simulated_results = Vec::with_capacity(iterations);
    
    // Parallel simulation using rayon
    simulated_results.par_extend(
        (0..iterations).into_par_iter().map(|_| {
            let mut iteration_result = 0.0;
            for &value in values {
                // Apply random variation within uncertainty range
                let variation = rand::random::<f64>() * 2.0 * uncertainty - uncertainty;
                iteration_result += value * (1.0 + variation);
            }
            iteration_result
        })
    );
    
    // Calculate statistics
    let mean = simulated_results.par_iter().sum::<f64>() / iterations as f64;
    let variance = simulated_results.par_iter()
        .map(|&x| (x - mean).powi(2))
        .sum::<f64>() / iterations as f64;
    let std_dev = variance.sqrt();
    
    // Store results
    unsafe {
        *results.offset(0) = mean;
        *results.offset(1) = std_dev;
        *results.offset(2) = simulated_results.iter().copied().fold(f64::INFINITY, f64::min);
        *results.offset(3) = simulated_results.iter().copied().fold(f64::NEG_INFINITY, f64::max);
    }
} 