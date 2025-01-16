from typing import Dict, List
import ctypes
from pathlib import Path

# Load Rust library
lib_path = (
    Path(__file__).parent.parent.parent.parent
    / "backend/rust_modules/target/release/libprotein_analysis.so"
)
lib = ctypes.CDLL(str(lib_path))


class TechnicalIntegrator:
    def __init__(self):
        # Configure Rust function signatures
        self.lib = lib
        self.lib.calculate_protein_recovery.argtypes = [
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
        ]
        self.lib.calculate_protein_recovery.restype = ctypes.c_double

        self.lib.analyze_particle_distribution.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
        ]

    def analyze_protein_recovery(
        self, protein_yield: float, protein_content: float, separation_efficiency: float
    ) -> float:
        """Calculate protein recovery using Rust implementation"""
        return self.lib.calculate_protein_recovery(
            ctypes.c_double(protein_yield),
            ctypes.c_double(protein_content),
            ctypes.c_double(separation_efficiency),
        )

    def analyze_particle_distribution(self, particles: List[float]) -> Dict[str, float]:
        """Analyze particle size distribution using Rust implementation"""
        arr = (ctypes.c_double * len(particles))(*particles)
        d10 = ctypes.c_double()
        d50 = ctypes.c_double()
        d90 = ctypes.c_double()

        self.lib.analyze_particle_distribution(
            arr, len(particles), ctypes.byref(d10), ctypes.byref(d50), ctypes.byref(d90)
        )

        return {
            "D0.1": d10.value,
            "D0.5": d50.value,
            "D0.9": d90.value,
            "distribution_width": (d90.value - d10.value) / d50.value,
        }
