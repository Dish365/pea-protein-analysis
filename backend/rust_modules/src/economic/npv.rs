use std::ffi::c_double;

#[no_mangle]
pub extern "C" fn calculate_npv(
    cash_flows: *const c_double,
    len: usize,
    discount_rate: c_double
) -> c_double {
    let flows = unsafe { std::slice::from_raw_parts(cash_flows, len) };
    
    flows.iter().enumerate()
        .map(|(i, &flow)| {
            flow / (1.0 + discount_rate).powi(i as i32)
        })
        .sum()
}

// Add a helper function for internal use
pub(crate) fn calculate_npv_from_slice(flows: &[f64], rate: f64) -> f64 {
    flows.iter().enumerate()
        .map(|(i, &flow)| {
            flow / (1.0 + rate).powi(i as i32)
        })
        .sum()
} 