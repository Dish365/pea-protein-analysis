import numpy as np
from typing import Dict, List, Optional
from scipy import stats
from backend.fastapi_app.process_analysis.services.rust_handler import RustHandler


class ParticleSizeAnalyzer:
    """
    Analyze particle size distribution of protein fractions.

    This class implements methods for analyzing particle size distributions in protein
    fractionation processes, including:
    - Weighted percentile calculations (D10, D50, D90)
    - Distribution statistics
    - Quality assessment
    - Surface area calculations

    Mathematical Background:
    ----------------------
    1. Weighted Percentiles:
       For a given percentile p, the weighted percentile Dp is calculated using:
       Dp = x₁ + (x₂ - x₁) * (p - F₁)/(F₂ - F₁)
       where:
       - x₁, x₂ are consecutive particle sizes
       - F₁, F₂ are cumulative weights at those sizes
       - p is the desired percentile (0.1 for D10, 0.5 for D50, 0.9 for D90)

    2. Span Calculation:
       span = (D90 - D10)/D50

    3. Coefficient of Variation:
       CV = (σw/μw) * 100%
       where:
       - σw is weighted standard deviation
       - μw is weighted mean

    4. Specific Surface Area (for spherical particles):
       SSA = (6/ρd)
       where:
       - ρ is particle density
       - d is particle diameter
    """

    def __init__(self):
        self.rust_handler = RustHandler()

    def analyze_distribution(
        self, particle_sizes: List[float], weights: Optional[List[float]] = None
    ) -> Dict[str, float]:
        """
        Analyze particle size distribution parameters using weighted statistics.

        Algorithm:
        1. Normalize weights to sum to 1
        2. Sort particle sizes and corresponding weights
        3. Calculate cumulative distribution
        4. Compute percentiles using linear interpolation
        5. Calculate weighted statistics

        Mathematical Details:
        -------------------
        1. Weight Normalization:
           w'ᵢ = wᵢ/Σwᵢ

        2. Cumulative Distribution:
           F(x) = Σw'ᵢ for all xᵢ ≤ x

        3. Weighted Mean:
           μw = Σ(xᵢw'ᵢ)

        4. Weighted Variance:
           σ²w = Σw'ᵢ(xᵢ - μw)²
           
        Uses Rust for computationally intensive calculations (percentiles and weighted statistics).
        Python handles data preparation and post-processing.

        Args:
            particle_sizes: List of particle sizes in μm
            weights: Optional weights for each particle size

        Returns:
            Dict containing:
            - D10: 10th percentile diameter
            - D50: Median diameter
            - D90: 90th percentile diameter
            - span: Distribution span
            - mean: Weighted mean diameter
            - std_dev: Weighted standard deviation
            - cv: Coefficient of variation
        """
        if weights is None:
            weights = np.ones(len(particle_sizes)) / len(particle_sizes)
        else:
            # Normalize weights to sum to 1
            weights = np.array(weights) / np.sum(weights)

        # Use Rust for computationally intensive calculations
        rust_results = self.rust_handler.analyze_particle_distribution(
            particle_sizes=particle_sizes,
            weights=weights
        )

        # Calculate span using Rust results
        span = (rust_results["D90"] - rust_results["D10"]) / rust_results["D50"] if rust_results["D50"] > 0 else float("inf")
        
        # Calculate CV using Rust results
        cv = (rust_results["std_dev"] / rust_results["mean"] * 100) if rust_results["mean"] > 0 else float("inf")

        return {
            "D10": rust_results["D10"],
            "D50": rust_results["D50"],
            "D90": rust_results["D90"],
            "span": span,
            "mean": rust_results["mean"],
            "std_dev": rust_results["std_dev"],
            "cv": cv
        }

    def evaluate_size_quality(
        self, distribution_params: Dict[str, float], target_ranges: Dict[str, tuple]
    ) -> Dict[str, float]:
        """
        Evaluate particle size quality against target ranges.

        Quality Score Calculation:
        ------------------------
        For each parameter:
        1. If value is within range:
           score = 100
        2. If value is outside range:
           score = max(0, 100 * (1 - |deviation|))
           where deviation is relative distance from nearest range boundary

        Overall quality is the arithmetic mean of individual scores.

        Args:
            distribution_params: Dict with distribution parameters
            target_ranges: Dict with (min, max) tuples for parameters

        Returns:
            Dict containing quality scores (0-100) for each parameter
            and overall quality score
        """
        quality_scores = {}

        for param, (min_val, max_val) in target_ranges.items():
            if param in distribution_params:
                value = distribution_params[param]
                if min_val <= value <= max_val:
                    quality_scores[param] = 100.0
                else:
                    # Calculate percentage deviation from range
                    if value < min_val:
                        deviation = (min_val - value) / min_val
                    else:
                        deviation = (value - max_val) / max_val
                    quality_scores[param] = max(0.0, 100.0 * (1.0 - deviation))

        # Calculate overall quality score
        if quality_scores:
            quality_scores["overall"] = np.mean(list(quality_scores.values()))

        return quality_scores

    def calculate_surface_area(
        self,
        particle_sizes: List[float],
        density: float,
        weights: Optional[List[float]] = None,
    ) -> Dict[str, float]:
        """
        Calculate specific surface area assuming spherical particles.

        Mathematical Formulas:
        --------------------
        For spherical particles:
        1. Surface Area (SA):
           SA = 4πr² = π(d)²

        2. Volume (V):
           V = (4/3)πr³ = (π/6)(d)³

        3. Specific Surface Area (SSA):
           SSA = Total Surface Area / (Total Volume * Density)
           SSA = 6/(ρd) for monodisperse spheres

        For polydisperse systems:
        SSA = Σ(wᵢSAᵢ) / (ρΣ(wᵢVᵢ))

        Args:
            particle_sizes: List of particle sizes in μm
            density: Particle density in g/cm³
            weights: Optional weights for each particle size

        Returns:
            Dict containing:
            - specific_surface_area: in cm²/g
            - total_surface_area: in cm²
            - mean_surface_area: weighted mean surface area
        """
        if weights is None:
            weights = np.ones(len(particle_sizes)) / len(particle_sizes)
        else:
            weights = np.array(weights) / np.sum(weights)

        # Convert μm to cm
        sizes_cm = np.array(particle_sizes) / 10000.0

        # Calculate surface areas and volumes (assuming spherical particles)
        surface_areas = 4.0 * np.pi * (sizes_cm / 2.0) ** 2  # SA = 4πr²
        volumes = (4.0 / 3.0) * np.pi * (sizes_cm / 2.0) ** 3  # V = (4/3)πr³

        # Calculate weighted averages
        total_surface_area = np.sum(surface_areas * weights)
        total_volume = np.sum(volumes * weights)

        # Calculate specific surface area (cm²/g)
        specific_surface_area = total_surface_area / (total_volume * density)

        return {
            "specific_surface_area": specific_surface_area,
            "total_surface_area": total_surface_area,
            "mean_surface_area": np.average(surface_areas, weights=weights),
        }
