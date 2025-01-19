use std::ffi::c_double;

#[no_mangle]
pub extern "C" fn calculate_allocation(
    impacts: *const c_double,
    values: *const c_double,
    len: usize,
    allocation_factors: *mut c_double
) -> bool {
    let impacts_slice = unsafe { std::slice::from_raw_parts(impacts, len) };
    let values_slice = unsafe { std::slice::from_raw_parts(values, len) };
    let factors_slice = unsafe { std::slice::from_raw_parts_mut(allocation_factors, len) };
    
    // Calculate total value
    let total_value: f64 = values_slice.iter().sum();
    
    if total_value <= 0.0 {
        return false;
    }
    
    // Calculate allocation factors
    for i in 0..len {
        factors_slice[i] = values_slice[i] / total_value;
    }
    
    // Apply allocation factors to impacts
    for i in 0..len {
        factors_slice[i] *= impacts_slice[i];
    }
    
    true
}

#[no_mangle]
pub extern "C" fn calculate_hybrid_allocation(
    mass_factors: *const c_double,
    economic_factors: *const c_double,
    len: usize,
    weight: c_double,
    results: *mut c_double
) -> bool {
    let mass_slice = unsafe { std::slice::from_raw_parts(mass_factors, len) };
    let economic_slice = unsafe { std::slice::from_raw_parts(economic_factors, len) };
    let results_slice = unsafe { std::slice::from_raw_parts_mut(results, len) };
    
    // Weight should be between 0 and 1
    let w = weight.max(0.0).min(1.0);
    
    // Calculate hybrid factors
    for i in 0..len {
        results_slice[i] = w * mass_slice[i] + (1.0 - w) * economic_slice[i];
    }
    
    true
} 