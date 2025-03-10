import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from backend.fastapi_app.models.protein_analysis import ProcessType
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
    - Moisture content tracking and validation

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

    Moisture Content Requirements:
    ---------------------------
    1. Pre-treatment:
       - RF treatment: Initial ≥ 13.6%
       - IR treatment: Initial = 15.5%

    2. Post-treatment:
       - RF treated: ~10.2%
       - IR treated: ~10.6%

    3. Processing:
       - Required range: 12-13% for optimal dehulling and fractionation
    """

    def __init__(self):
        self.rust_handler = RustHandler()
        self.moisture_content = None  # Current moisture content
        self.treatment_type = None    # Current treatment type

    def check_moisture_requirements(
        self, 
        moisture_level: float, 
        stage: str = "processing",
        treatment: Optional[ProcessType] = None
    ) -> Tuple[bool, str]:
        """
        Verify if moisture content meets requirements for different processing stages.

        Args:
            moisture_level: Current moisture content percentage
            stage: Processing stage ('pre_treatment', 'post_treatment', 'processing')
            treatment: Treatment type ('RF' or 'IR') if applicable

        Returns:
            Tuple of (bool, str) indicating if requirements are met and any message
        """
        if stage == "pre_treatment":
            if treatment == ProcessType.RF:
                if moisture_level >= 13.6:
                    return True, "Sufficient moisture for RF treatment"
                return False, f"Insufficient moisture for RF treatment (need ≥13.6%, got {moisture_level}%)"
            elif treatment == ProcessType.IR:
                if abs(moisture_level - 15.5) <= 0.5:
                    return True, "Optimal moisture for IR treatment"
                return False, f"Suboptimal moisture for IR treatment (need 15.5%, got {moisture_level}%)"
        
        elif stage == "post_treatment":
            expected = 10.2 if treatment == ProcessType.RF else 10.6
            if abs(moisture_level - expected) <= 0.5:
                return True, f"Expected post-{treatment.value} moisture content"
            return False, f"Unexpected post-{treatment.value} moisture content (expected ~{expected}%, got {moisture_level}%)"
        
        elif stage == "processing":
            if 12.0 <= moisture_level <= 13.0:
                return True, "Optimal moisture for processing"
            return False, f"Suboptimal processing moisture (need 12-13%, got {moisture_level}%)"
        
        return False, "Invalid stage specified"

    def process_sample(
        self,
        particle_data: Dict[str, Any],
        treatment_type: Optional[ProcessType] = None
    ) -> Dict:
        """
        Process sample with moisture content validation and particle analysis.
        
        Args:
            particle_data: Dictionary containing particle size distribution and moisture data
            treatment_type: Optional pre-treatment type ('RF' or 'IR')
            
        Returns:
            Dict containing distribution analysis results, surface area, and moisture status
        """
        # Validate and process particle data
        validated_data = self.validate_particle_data(particle_data)
        
        self.moisture_content = validated_data["initial_moisture"]
        self.treatment_type = treatment_type
        
        moisture_status = {}
        
        if treatment_type:
            # Check pre-treatment moisture
            valid, msg = self.check_moisture_requirements(
                validated_data["initial_moisture"],
                "pre_treatment",
                treatment_type
            )
            moisture_status["pre_treatment"] = {
                "valid": valid,
                "message": msg,
                "moisture": validated_data["initial_moisture"]
            }
            
            # Update to post-treatment moisture
            self.moisture_content = validated_data["final_moisture"]
            valid, msg = self.check_moisture_requirements(
                self.moisture_content,
                "post_treatment",
                treatment_type
            )
            moisture_status["post_treatment"] = {
                "valid": valid,
                "message": msg,
                "moisture": self.moisture_content
            }
            
        # Check processing moisture requirements
        valid, msg = self.check_moisture_requirements(
            self.moisture_content,
            "processing"
        )
        moisture_status["processing"] = {
            "valid": valid,
            "message": msg,
            "moisture": self.moisture_content
        }
        
        # Perform distribution analysis
        distribution_results = self.analyze_distribution(
            validated_data["sizes"],
            validated_data["weights"]
        )
        
        # Calculate surface area
        surface_area_results = self.calculate_surface_area(
            validated_data["sizes"],
            validated_data["density"],
            validated_data["weights"]
        )
        
        # Combine results
        return {
            **distribution_results,
            **surface_area_results,
            "moisture_status": moisture_status,
            "current_moisture": self.moisture_content,
            "percentiles": validated_data["percentiles"]
        }

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

    def validate_particle_data(self, particle_data: Dict) -> Dict[str, Any]:
        """
        Validate and process particle size data structure.
        
        Args:
            particle_data: Dictionary containing:
                - sizes: List of particle sizes (optional)
                - weights: List of weights (optional)
                - percentiles: Dict with d10, d50, d90
                - density: Particle density
                - initial_moisture: Initial moisture content
                - final_moisture: Final moisture content
                
        Returns:
            Dict with validated and processed data
        """
        # Validate percentiles
        percentiles = particle_data.get("percentiles", {})
        if not all(key in percentiles for key in ["d10", "d50", "d90"]):
            raise ValueError("Missing required percentile values (d10, d50, d90)")
            
        # If no distribution data provided, create synthetic distribution
        if not particle_data.get("sizes"):
            # Create log-normal distribution based on percentiles
            sizes = self.rust_handler.generate_distribution(
                d10=percentiles["d10"],
                d50=percentiles["d50"],
                d90=percentiles["d90"],
                num_points=100
            )
            weights = None  # Use uniform weights
        else:
            sizes = particle_data["sizes"]
            weights = particle_data.get("weights")
            
        # Validate density
        density = particle_data.get("density", 1.5)  # Default protein particle density
        if density <= 0:
            raise ValueError("Particle density must be positive")
            
        return {
            "sizes": sizes,
            "weights": weights,
            "percentiles": percentiles,
            "density": density,
            "initial_moisture": particle_data["initial_moisture"],
            "final_moisture": particle_data["final_moisture"]
        }
