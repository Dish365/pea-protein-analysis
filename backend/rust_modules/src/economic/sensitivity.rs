use rayon::prelude::*;

/// Run sensitivity analysis on cash flows
/// 
/// # Safety
/// This function is unsafe because it works with raw pointers.
/// The caller must ensure that:
/// - base_values points to a valid array of f64 with length len
/// - results points to a valid array of f64 with length steps + 1
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
    // Convert input slice safely
    let values = unsafe { std::slice::from_raw_parts(base_values, len) };
    let step_size = (range_max - range_min) / (steps as f64);
    
    // Parallel sensitivity analysis using rayon
    let sensitivity_results: Vec<f64> = (0..=steps)
        .into_par_iter()
        .map(|i| {
            let factor = range_min + (i as f64) * step_size;
            
            // Handle different variable types
            match variable_index {
                0 => {
                    // Discount rate sensitivity - apply to all cash flows
                    calculate_npv_with_rate(values, factor)
                },
                _ => {
                    // Production volume or other factor sensitivity
                    let mut modified_values = values.to_vec();
                    for j in 1..modified_values.len() {
                        modified_values[j] *= factor;
                    }
                    calculate_npv_with_rate(&modified_values, 0.1) // Use default discount rate
                }
            }
        })
        .collect();
    
    // Store results safely
    unsafe {
        for (i, &value) in sensitivity_results.iter().enumerate() {
            *results.add(i) = value;
        }
    }
}

fn calculate_npv_with_rate(cash_flows: &[f64], discount_rate: f64) -> f64 {
    let initial_investment = cash_flows[0];
    
    // Calculate NPV excluding initial investment
    let discounted_flows: f64 = cash_flows[1..]
        .iter()
        .enumerate()
        .map(|(year, &flow)| {
            flow / (1.0 + discount_rate).powi((year + 1) as i32)
        })
        .sum();
    
    initial_investment + discounted_flows
} 