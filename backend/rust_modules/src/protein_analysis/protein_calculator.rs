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
) -> bool {
    if sizes.is_null() || weights.is_null() || len == 0 {
        return false;
    }

    // Convert raw pointers to slices with safety checks
    let (sizes, weights) = match (
        unsafe { std::slice::from_raw_parts(sizes, len) },
        unsafe { std::slice::from_raw_parts(weights, len) }
    ) {
        (s, w) if s.iter().any(|x| x.is_nan()) || w.iter().any(|x| x.is_nan()) => return false,
        (s, w) => (s, w),
    };
    
    // Pre-allocate with capacity
    let mut size_weight: Vec<(f64, f64)> = Vec::with_capacity(len);
    size_weight.extend(sizes.iter().zip(weights.iter()).map(|(&s, &w)| (s, w)));
    
    // Sort by size using unstable sort (faster)
    size_weight.sort_unstable_by(|a, b| a.0.partial_cmp(&b.0).unwrap_or(Ordering::Equal));
    
    // Calculate total weight once
    let total_weight: f64 = weights.iter().sum();
    if total_weight <= 0.0 {
        return false;
    }

    // Pre-allocate cumulative weights
    let mut cumulative = Vec::with_capacity(len);
    let mut cum_sum = 0.0;
    let weight_factor = 1.0 / total_weight;
    
    // Optimize cumulative weight calculation
    for (_, w) in &size_weight {
        cum_sum += w * weight_factor;
        cumulative.push(cum_sum);
    }
    
    // Calculate weighted mean with single pass
    let weighted_mean: f64 = size_weight.iter()
        .fold(0.0, |acc, (s, w)| acc + s * (w * weight_factor));
    
    // Calculate weighted variance with single pass
    let weighted_var: f64 = size_weight.iter()
        .fold(0.0, |acc, (s, w)| {
            let diff = s - weighted_mean;
            acc + diff * diff * (w * weight_factor)
        });
    
    let weighted_std = weighted_var.sqrt();
    
    // Optimize percentile calculation with binary search
    let get_percentile = |p: f64| {
        match cumulative.binary_search_by(|&x| x.partial_cmp(&p).unwrap_or(Ordering::Equal)) {
            Ok(idx) => size_weight[idx].0,
            Err(idx) if idx == 0 => size_weight[0].0,
            Err(idx) if idx >= len => size_weight[len-1].0,
            Err(idx) => {
                let (x0, x1) = (size_weight[idx-1].0, size_weight[idx].0);
                let (y0, y1) = (cumulative[idx-1], cumulative[idx]);
                x0 + (x1 - x0) * (p - y0) / (y1 - y0)
            }
        }
    };
    
    // Calculate percentiles safely
    unsafe {
        *d10 = get_percentile(0.1);
        *d50 = get_percentile(0.5);
        *d90 = get_percentile(0.9);
        *mean = weighted_mean;
        *std_dev = weighted_std;
    }
    
    true
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