use rayon::prelude::*;

#[no_mangle]
pub extern "C" fn run_sensitivity_analysis(
    base_values: *const f64,
    len: usize,
    variable_index: usize,
    range_min: f64,
    range_max: f64,
    steps: usize,
    results: *mut f64
) {
    let values = unsafe { std::slice::from_raw_parts(base_values, len) };
    let step_size = (range_max - range_min) / (steps as f64);
    
    // Parallel sensitivity analysis using rayon
    let sensitivity_results: Vec<f64> = (0..=steps)
        .into_par_iter()
        .map(|i| {
            let mut modified_values = values.to_vec();
            let factor = range_min + (i as f64) * step_size;
            modified_values[variable_index] *= factor;
            
            // Calculate NPV for modified values
            modified_values.iter().enumerate()
                .map(|(i, &value)| value / (1.1f64.powi(i as i32)))
                .sum()
        })
        .collect();
    
    // Store results
    unsafe {
        for (i, &value) in sensitivity_results.iter().enumerate() {
            *results.offset(i as isize) = value;
        }
    }
} 