use std::ffi::{c_double, c_void};

#[no_mangle]
pub extern "C" fn calculate_protein_recovery(
    protein_yield: c_double,
    protein_content: c_double,
    separation_efficiency: c_double
) -> c_double {
    (protein_yield * protein_content * separation_efficiency) / 100.0
}

#[no_mangle]
pub extern "C" fn analyze_particle_distribution(
    particles: *const c_double,
    len: usize,
    d10: *mut c_double,
    d50: *mut c_double,
    d90: *mut c_double
) -> c_void {
    let slice = unsafe { std::slice::from_raw_parts(particles, len) };
    let mut vec = slice.to_vec();
    vec.sort_by(|a, b| a.partial_cmp(b).unwrap());
    
    unsafe {
        *d10 = percentile(&vec, 10.0);
        *d50 = percentile(&vec, 50.0);
        *d90 = percentile(&vec, 90.0);
    }
}

fn percentile(data: &Vec<f64>, p: f64) -> f64 {
    let idx = (p / 100.0 * (data.len() - 1) as f64).round() as usize;
    data[idx]
} 