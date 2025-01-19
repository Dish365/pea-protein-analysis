use std::ffi::{c_double};
use std::cmp::Ordering;

#[no_mangle]
pub extern "C" fn calculate_protein_recovery(
    protein_yield: c_double,
    protein_content: c_double,
    separation_efficiency: c_double
) -> c_double {
    (protein_yield * protein_content * separation_efficiency) / 100.0
}

/// Calculate weighted percentiles and statistics for particle size distribution
#[no_mangle]
pub extern "C" fn analyze_particle_distribution(
    sizes: *const f64,
    weights: *const f64,
    len: usize,
    d10: *mut f64,
    d50: *mut f64,
    d90: *mut f64,
    mean: *mut f64,
    std_dev: *mut f64
) {
    // Convert raw pointers to slices
    let sizes = unsafe { std::slice::from_raw_parts(sizes, len) };
    let weights = unsafe { std::slice::from_raw_parts(weights, len) };
    
    // Create mutable vectors for sorting
    let mut size_weight: Vec<(f64, f64)> = sizes.iter()
        .zip(weights.iter())
        .map(|(&s, &w)| (s, w))
        .collect();
    
    // Sort by size
    size_weight.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap_or(Ordering::Equal));
    
    // Calculate cumulative weights
    let total_weight: f64 = weights.iter().sum();
    let mut cumulative = Vec::with_capacity(len);
    let mut cum_sum = 0.0;
    
    for (_, w) in &size_weight {
        cum_sum += w / total_weight;
        cumulative.push(cum_sum);
    }
    
    // Calculate weighted mean
    let weighted_mean: f64 = size_weight.iter()
        .map(|(s, w)| s * (w / total_weight))
        .sum();
    
    // Calculate weighted variance and std dev
    let weighted_var: f64 = size_weight.iter()
        .map(|(s, w)| (s - weighted_mean) * (s - weighted_mean) * (w / total_weight))
        .sum();
    let weighted_std = weighted_var.sqrt();
    
    // Helper function for percentile calculation
    let get_percentile = |p: f64| {
        let idx = match cumulative.iter().position(|&x| x >= p) {
            Some(i) => i,
            None => return size_weight.last().unwrap().0,
        };
        
        if idx == 0 {
            return size_weight[0].0;
        }
        
        let (x0, x1) = (size_weight[idx-1].0, size_weight[idx].0);
        let (y0, y1) = (cumulative[idx-1], cumulative[idx]);
        
        x0 + (x1 - x0) * (p - y0) / (y1 - y0)
    };
    
    // Calculate D10, D50, D90
    unsafe {
        *d10 = get_percentile(0.1);
        *d50 = get_percentile(0.5);
        *d90 = get_percentile(0.9);
        *mean = weighted_mean;
        *std_dev = weighted_std;
    }
}

#[no_mangle]
pub extern "C" fn calculate_separation_efficiency(
    input_mass: c_double,
    output_mass: c_double,
    input_concentration: c_double,
    output_concentration: c_double
) -> c_double {
    if input_mass <= 0.0 || input_concentration <= 0.0 {
        return 0.0;
    }

    let efficiency = (output_mass * output_concentration) / (input_mass * input_concentration);
    
    // Clamp between 0 and 1
    efficiency.max(0.0).min(1.0)
} 