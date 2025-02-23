use rand_distr::{Distribution, Normal};
use rand::{SeedableRng, rngs::StdRng};
use rayon::prelude::*;

#[no_mangle]
pub extern "C" fn run_economic_monte_carlo(
    base_values: *const f64,
    len: usize,
    iterations: usize,
    price_uncertainty: f64,
    cost_uncertainty: f64,
    production_uncertainty: f64,
    seed: u64,
    discount_rate: f64,
    results: *mut f64
) -> bool {
    // Safety checks
    if base_values.is_null() || results.is_null() || len == 0 || iterations == 0 {
        return false;
    }

    let values = unsafe { std::slice::from_raw_parts(base_values, len) };
    let mut simulated_npvs = Vec::with_capacity(iterations);
    
    // Create distributions for each uncertainty type
    let price_dist = match Normal::new(0.0, price_uncertainty) {
        Ok(dist) => dist,
        Err(_) => return false,
    };
    let cost_dist = match Normal::new(0.0, cost_uncertainty) {
        Ok(dist) => dist,
        Err(_) => return false,
    };
    let production_dist = match Normal::new(0.0, production_uncertainty) {
        Ok(dist) => dist,
        Err(_) => return false,
    };

    simulated_npvs.par_extend(
        (0..iterations).into_par_iter().map(|i| {
            // Create a unique seed for each iteration
            let iteration_seed = seed.wrapping_add(i as u64);
            let mut rng = StdRng::seed_from_u64(iteration_seed);
            
            values.iter().enumerate().map(|(i, &value)| {
                if i == 0 {
                    // Initial investment - no uncertainty applied
                    value
                } else {
                    let production_var = production_dist.sample(&mut rng);
                    let adjusted_value = if value > 0.0 {
                        // Apply price uncertainty to positive cash flows (revenue)
                        let price_var = price_dist.sample(&mut rng);
                        value * (1.0 + price_var) * (1.0 + production_var)
                    } else {
                        // Apply cost uncertainty to negative cash flows (costs)
                        let cost_var = cost_dist.sample(&mut rng);
                        value * (1.0 + cost_var) * (1.0 + production_var)
                    };
                    adjusted_value / ((1.0 + discount_rate).powi(i as i32))
                }
            }).sum::<f64>()
        })
    );
    
    // Calculate statistics
    let mean = simulated_npvs.par_iter().sum::<f64>() / iterations as f64;
    let variance = simulated_npvs.par_iter()
        .map(|&x| (x - mean).powi(2))
        .sum::<f64>() / iterations as f64;
    let std_dev = variance.sqrt();
    
    // Find min and max values
    let min_val = simulated_npvs.iter().copied().fold(f64::INFINITY, f64::min);
    let max_val = simulated_npvs.iter().copied().fold(f64::NEG_INFINITY, f64::max);
    
    // Store results safely
    unsafe {
        *results.offset(0) = mean;
        *results.offset(1) = std_dev;
        *results.offset(2) = min_val;
        *results.offset(3) = max_val;
    }
    
    true
} 