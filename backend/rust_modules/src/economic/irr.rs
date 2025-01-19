use std::ffi::c_double;
use super::npv::calculate_npv_from_slice;

#[no_mangle]
pub extern "C" fn calculate_irr(
    cash_flows: *const c_double,
    len: usize,
    result: *mut c_double
) -> bool {
    let flows = unsafe { std::slice::from_raw_parts(cash_flows, len) };
    
    // Newton-Raphson method for IRR calculation
    let mut rate = 0.1;  // Initial guess
    let max_iterations = 100;
    let tolerance = 1e-6;

    for _ in 0..max_iterations {
        let npv = calculate_npv_from_slice(flows, rate);
        if npv.abs() < tolerance {
            unsafe { *result = rate; }
            return true;
        }
        
        // Calculate derivative
        let delta = 0.0001;
        let derivative = (calculate_npv_from_slice(flows, rate + delta) - npv) / delta;
        
        // Update rate
        rate = rate - npv / derivative;
    }
    
    false  // Failed to converge
} 