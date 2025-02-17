use rayon::prelude::*;
use crate::npv::calculate_npv;
use std::ffi::c_double;

#[derive(Debug)]
pub enum SensitivityVariable {
    DiscountRate = 0,
    ProductionVolume = 1,
    OperatingCosts = 2,
    Revenue = 3,
}

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
            
            // Match on SensitivityVariable
            match variable_index {
                0 => calculate_npv_with_rate(values, factor), // Discount rate
                1 => calculate_with_volume_factor(values, factor), // Production volume
                2 => calculate_with_opex_factor(values, factor), // Operating costs
                3 => calculate_with_revenue_factor(values, factor), // Revenue
                _ => calculate_npv_with_rate(values, 0.1) // Default to discount rate if unknown
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
    calculate_npv(
        cash_flows.as_ptr(),
        cash_flows.len(),
        discount_rate
    )
}

fn calculate_npv_with_modified_flows(cash_flows: &[f64], modifier: f64, discount_rate: f64) -> f64 {
    let modified_flows: Vec<f64> = cash_flows.iter()
        .enumerate()
        .map(|(i, &v)| if i == 0 { v } else { v * modifier })
        .collect();
    
    calculate_npv(
        modified_flows.as_ptr(),
        modified_flows.len(),
        discount_rate
    )
}

fn calculate_with_volume_factor(cash_flows: &[f64], factor: f64) -> f64 {
    let initial_investment = cash_flows[0];
    let modified_flows: Vec<f64> = std::iter::once(initial_investment)
        .chain(cash_flows[1..].iter().map(|&cf| cf * factor))
        .collect();
    
    calculate_npv(
        modified_flows.as_ptr(),
        modified_flows.len(),
        0.1
    )
}

fn calculate_with_opex_factor(cash_flows: &[f64], factor: f64) -> f64 {
    let initial_investment = cash_flows[0];
    let modified_flows: Vec<f64> = std::iter::once(initial_investment)
        .chain(cash_flows[1..].iter().map(|&cf| {
            if cf < 0.0 { cf * factor } else { cf } // Only modify negative flows (costs)
        }))
        .collect();
    
    calculate_npv(
        modified_flows.as_ptr(),
        modified_flows.len(),
        0.1
    )
}

fn calculate_with_revenue_factor(cash_flows: &[f64], factor: f64) -> f64 {
    let initial_investment = cash_flows[0];
    let modified_flows: Vec<f64> = std::iter::once(initial_investment)
        .chain(cash_flows[1..].iter().map(|&cf| {
            if cf > 0.0 { cf * factor } else { cf } // Only modify positive flows (revenue)
        }))
        .collect();
    
    calculate_npv(
        modified_flows.as_ptr(),
        modified_flows.len(),
        0.1
    )
}

#[no_mangle]
pub extern "C" fn analyze_sensitivity(
    cash_flows: *const c_double,
    len: usize,
    discount_rate: c_double,
    _production_volume: c_double,  // Prefix with _ to indicate intentionally unused
    _operating_costs: c_double,    // Prefix with _ to indicate intentionally unused
    _revenue: c_double            // Prefix with _ to indicate intentionally unused
) -> *mut c_double {
    let cash_flows_slice = unsafe {
        std::slice::from_raw_parts(cash_flows, len)
    };
    
    // Calculate base NPV
    let base_npv = calculate_npv_with_rate(cash_flows_slice, discount_rate);
    
    // Calculate NPV with modified discount rate
    let dr_low = discount_rate * 0.8;
    let dr_high = discount_rate * 1.2;
    let npv_dr_low = calculate_npv_with_rate(cash_flows_slice, dr_low);
    let npv_dr_high = calculate_npv_with_rate(cash_flows_slice, dr_high);
    
    // Calculate NPV with modified production volume
    let pv_low = calculate_npv_with_modified_flows(cash_flows_slice, 0.8, discount_rate);
    let pv_high = calculate_npv_with_modified_flows(cash_flows_slice, 1.2, discount_rate);
    
    // Calculate NPV with modified operating costs
    let opex_low = calculate_npv_with_modified_flows(cash_flows_slice, 0.8, discount_rate);
    let opex_high = calculate_npv_with_modified_flows(cash_flows_slice, 1.2, discount_rate);
    
    // Calculate NPV with modified revenue
    let rev_low = calculate_npv_with_modified_flows(cash_flows_slice, 0.8, discount_rate);
    let rev_high = calculate_npv_with_modified_flows(cash_flows_slice, 1.2, discount_rate);
    
    // Create results array
    let results = vec![
        base_npv,
        npv_dr_low, npv_dr_high,
        pv_low, pv_high,
        opex_low, opex_high,
        rev_low, rev_high
    ];
    
    // Convert to raw pointer
    let ptr = results.as_ptr() as *mut c_double;
    std::mem::forget(results);  // Prevent deallocation
    ptr
} 