use std::ffi::c_double;
use rayon::prelude::*;

#[no_mangle]
pub extern "C" fn matrix_multiply(
    a: *const c_double,
    b: *const c_double,
    result: *mut c_double,
    m: usize,
    n: usize,
    p: usize
) {
    let a_slice = unsafe { std::slice::from_raw_parts(a, m * n) };
    let b_slice = unsafe { std::slice::from_raw_parts(b, n * p) };
    let result_slice = unsafe { std::slice::from_raw_parts_mut(result, m * p) };
    
    // Parallel matrix multiplication using rayon
    result_slice.par_chunks_mut(p).enumerate().for_each(|(i, row)| {
        for j in 0..p {
            let mut sum = 0.0;
            for k in 0..n {
                sum += a_slice[i * n + k] * b_slice[k * p + j];
            }
            row[j] = sum;
        }
    });
}

#[no_mangle]
pub extern "C" fn matrix_inverse(
    matrix: *mut c_double,
    n: usize
) -> bool {
    let slice = unsafe { std::slice::from_raw_parts_mut(matrix, n * n) };
    
    // Create augmented matrix [A|I]
    let mut augmented = vec![0.0; n * 2 * n];
    for i in 0..n {
        for j in 0..n {
            augmented[i * (2 * n) + j] = slice[i * n + j];
        }
        augmented[i * (2 * n) + n + i] = 1.0;
    }
    
    // Gaussian elimination with partial pivoting
    for i in 0..n {
        // Find pivot
        let mut max_val = augmented[i * (2 * n) + i].abs();
        let mut max_row = i;
        for j in (i + 1)..n {
            let val = augmented[j * (2 * n) + i].abs();
            if val > max_val {
                max_val = val;
                max_row = j;
            }
        }
        
        if max_val < 1e-10 {
            return false;  // Matrix is singular
        }
        
        // Swap rows if necessary
        if max_row != i {
            for j in 0..(2 * n) {
                augmented.swap(i * (2 * n) + j, max_row * (2 * n) + j);
            }
        }
        
        // Scale row
        let pivot = augmented[i * (2 * n) + i];
        for j in 0..(2 * n) {
            augmented[i * (2 * n) + j] /= pivot;
        }
        
        // Eliminate column
        for j in 0..n {
            if j != i {
                let factor = augmented[j * (2 * n) + i];
                for k in 0..(2 * n) {
                    augmented[j * (2 * n) + k] -= factor * augmented[i * (2 * n) + k];
                }
            }
        }
    }
    
    // Extract inverse
    for i in 0..n {
        for j in 0..n {
            slice[i * n + j] = augmented[i * (2 * n) + n + j];
        }
    }
    
    true
} 