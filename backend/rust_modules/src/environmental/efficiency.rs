use std::ffi::c_double;

#[no_mangle]
pub extern "C" fn calculate_efficiency(
    economic_value: c_double,
    environmental_impact: c_double
) -> c_double {
    if environmental_impact <= 0.0 {
        return 0.0;
    }
    
    economic_value / environmental_impact
}

#[no_mangle]
pub extern "C" fn calculate_eco_efficiency_matrix(
    economic_values: *const c_double,
    environmental_impacts: *const c_double,
    len: usize,
    results: *mut c_double
) -> bool {
    let values_slice = unsafe { std::slice::from_raw_parts(economic_values, len) };
    let impacts_slice = unsafe { std::slice::from_raw_parts(environmental_impacts, len) };
    let results_slice = unsafe { std::slice::from_raw_parts_mut(results, len) };
    
    for i in 0..len {
        if impacts_slice[i] <= 0.0 {
            results_slice[i] = 0.0;
        } else {
            results_slice[i] = values_slice[i] / impacts_slice[i];
        }
    }
    
    true
} 