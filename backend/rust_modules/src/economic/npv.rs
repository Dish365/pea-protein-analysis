use std::ffi::c_double;

#[no_mangle]
pub extern "C" fn calculate_npv(
    cash_flows: *const c_double,
    len: usize,
    discount_rate: c_double
) -> c_double {
    // Safety check for null pointer
    if cash_flows.is_null() || len == 0 {
        return 0.0;
    }

    let cash_flows_slice = unsafe {
        std::slice::from_raw_parts(cash_flows, len)
    };
    
    // Calculate NPV using the helper function
    calculate_npv_from_slice(cash_flows_slice, discount_rate)
}

// Helper function for internal use that handles the actual NPV calculation
pub(crate) fn calculate_npv_from_slice(flows: &[f64], rate: f64) -> f64 {
    if flows.is_empty() {
        return 0.0;
    }

    flows.iter()
        .enumerate()
        .map(|(year, &flow)| {
            // Handle edge case where rate is very close to -1
            if (1.0 + rate).abs() < f64::EPSILON {
                return 0.0;
            }
            flow / (1.0 + rate).powi(year as i32)
        })
        .sum()
} 