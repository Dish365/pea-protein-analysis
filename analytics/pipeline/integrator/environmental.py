from typing import Dict, List
import ctypes
from pathlib import Path

# Load Rust library
lib_path = (
    Path(__file__).parent.parent.parent.parent
    / "backend/rust_modules/target/release/libmatrix_ops.so"
)
lib = ctypes.CDLL(str(lib_path))


class EnvironmentalIntegrator:
    def __init__(self):
        # Configure Rust function signatures
        self.lib = lib
        self.lib.matrix_multiply.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
        ]

        self.lib.matrix_inverse.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
        ]
        self.lib.matrix_inverse.restype = ctypes.c_bool

    def calculate_impact_matrix(
        self, process_matrix: List[List[float]], impact_factors: List[List[float]]
    ) -> List[List[float]]:
        """Calculate environmental impact matrix using Rust implementation"""
        m = len(process_matrix)
        n = len(process_matrix[0])
        p = len(impact_factors[0])

        # Flatten matrices
        a = (ctypes.c_double * (m * n))(*[x for row in process_matrix for x in row])
        b = (ctypes.c_double * (n * p))(*[x for row in impact_factors for x in row])
        result = (ctypes.c_double * (m * p))()

        self.lib.matrix_multiply(a, b, result, m, n, p)

        # Reshape result
        return [[result[i * p + j] for j in range(p)] for i in range(m)]

    def calculate_allocation_factors(
        self, correlation_matrix: List[List[float]]
    ) -> List[float]:
        """Calculate allocation factors using matrix inversion"""
        n = len(correlation_matrix)
        matrix = (ctypes.c_double * (n * n))(
            *[x for row in correlation_matrix for x in row]
        )

        if not self.lib.matrix_inverse(matrix, n):
            raise ValueError("Matrix is singular, cannot calculate allocation factors")

        # Extract diagonal elements as allocation factors
        return [matrix[i * n + i] for i in range(n)]

    def normalize_impacts(
        self, impacts: List[float], reference_values: List[float]
    ) -> Dict[str, float]:
        """Normalize environmental impacts against reference values"""
        if len(impacts) != len(reference_values):
            raise ValueError("Impact and reference lists must have same length")

        normalized = []
        for impact, ref in zip(impacts, reference_values):
            if ref == 0:
                normalized.append(0.0)
            else:
                normalized.append(impact / ref)

        return {
            "normalized_impacts": normalized,
            "total_normalized_impact": sum(normalized),
        }
