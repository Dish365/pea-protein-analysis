import numpy as np
from typing import Dict, Optional


class ProteinRecoveryCalculator:
    """
    Calculate and analyze protein recovery metrics in fractionation processes.

     This class implements methods for analyzing protein recovery and yield in
     fractionation processes, including:
     - Recovery rate calculation
     - Protein loss tracking
     - Concentration factor analysis
     - Theoretical and practical yield estimation

     Mathematical Background:
     ----------------------
     1. Recovery Rate (R):
        R = (Mf * Cf)/(Mi * Ci) * 100%
        where:
        - Mf = Final mass
        - Cf = Final protein concentration
        - Mi = Initial mass
        - Ci = Initial protein concentration

     2. Concentration Factor (CF):
        CF = Cf/Ci
        where:
        - Cf = Final protein concentration
        - Ci = Initial protein concentration

     3. Theoretical Yield (Yt):
        Yt = (Ci/Ct) * 100%
        where:
        - Ci = Initial protein concentration
        - Ct = Target protein concentration

     4. Protein Mass Balance:
        Pi = Mi * (Ci/100)  # Initial protein mass
        Pf = Mf * (Cf/100)  # Final protein mass
        Pl = Pi - Pf        # Protein loss
    """

    def __init__(self, initial_protein_content: float):
        """
        Initialize calculator with initial protein content.

        Args:
            initial_protein_content (float): Initial protein content in percentage

        Raises:
            ValueError: If initial_protein_content is not between 0 and 100
        """
        if not 0 < initial_protein_content <= 100:
            raise ValueError("Initial protein content must be between 0 and 100%")
        self.initial_protein_content = initial_protein_content

    def calculate_recovery(
        self, output_mass: float, input_mass: float, output_protein_content: float
    ) -> Dict[str, float]:
        """
        Calculate protein recovery rate and related metrics.

        Algorithm:
        1. Calculate initial and final protein masses
        2. Calculate recovery rate
        3. Calculate protein loss
        4. Calculate concentration factor

        Mathematical Details:
        -------------------
        1. Protein Mass Calculation:
           Pi = Mi * (Ci/100)  # Initial protein mass
           Pf = Mf * (Cf/100)  # Final protein mass

        2. Recovery Rate:
           R = (Pf/Pi) * 100%

        3. Concentration Factor:
           CF = Cf/Ci

        Args:
            output_mass: Mass of output product in kg
            input_mass: Mass of input material in kg
            output_protein_content: Protein content in output in percentage

        Returns:
            Dict containing:
            - recovery_rate: Percentage of protein recovered
            - protein_loss: Amount of protein lost in kg
            - concentration_factor: Ratio of output to input concentration

        Raises:
            ValueError: If input parameters are invalid
        """
        # Validate inputs
        if output_mass <= 0 or input_mass <= 0:
            raise ValueError("Masses must be positive")
        if not 0 < output_protein_content <= 100:
            raise ValueError("Protein content must be between 0 and 100%")

        # Calculate initial protein mass
        initial_protein_mass = input_mass * (self.initial_protein_content / 100)

        # Calculate final protein mass
        final_protein_mass = output_mass * (output_protein_content / 100)

        # Calculate recovery rate
        recovery_rate = (final_protein_mass / initial_protein_mass) * 100

        # Calculate protein loss
        protein_loss = initial_protein_mass - final_protein_mass

        # Calculate concentration factor
        concentration_factor = output_protein_content / self.initial_protein_content

        return {
            "recovery_rate": recovery_rate,
            "protein_loss": protein_loss,
            "concentration_factor": concentration_factor,
        }

    def estimate_yield(
        self, target_protein_content: float, efficiency_factor: Optional[float] = 0.95
    ) -> Dict[str, float]:
        """
        Estimate theoretical and practical yield for target protein content.

        Mathematical Background:
        ----------------------
        1. Theoretical Yield:
           Yt = (Ci/Ct) * 100%

        2. Practical Yield:
           Yp = Yt * η
           where:
           - η = efficiency factor (typically 0.90-0.98)

        The efficiency factor accounts for:
        - Process losses
        - Equipment inefficiencies
        - Non-ideal separation

        Args:
            target_protein_content: Desired protein content in percentage
            efficiency_factor: Process efficiency factor (default: 0.95)

        Returns:
            Dict containing:
            - theoretical_yield: Maximum possible yield in kg/kg
            - expected_yield: Practical yield considering efficiency

        Raises:
            ValueError: If target_protein_content is invalid
        """
        # Validate inputs
        if not 0 < target_protein_content <= 100:
            raise ValueError("Target protein content must be between 0 and 100%")
        if not 0 < efficiency_factor <= 1:
            raise ValueError("Efficiency factor must be between 0 and 1")

        # Calculate theoretical maximum yield
        theoretical_yield = (
            self.initial_protein_content / target_protein_content
        ) * 100

        # Apply efficiency factor for practical yield
        expected_yield = theoretical_yield * efficiency_factor

        return {
            "theoretical_yield": theoretical_yield,
            "expected_yield": expected_yield,
        }

    def analyze_process_efficiency(
        self, actual_yield: float, target_protein_content: float
    ) -> Dict[str, float]:
        """
        Analyze process efficiency by comparing actual to theoretical yield.

        Mathematical Details:
        -------------------
        1. Process Efficiency:
           η = (Ya/Yt) * 100%
           where:
           - Ya = Actual yield
           - Yt = Theoretical yield

        2. Yield Gap:
           G = Yt - Ya

        Args:
            actual_yield: Achieved yield in kg/kg
            target_protein_content: Target protein content in percentage

        Returns:
            Dict containing:
            - process_efficiency: Actual vs theoretical efficiency
            - yield_gap: Difference between theoretical and actual yield
            - improvement_potential: Percentage points available for improvement
        """
        theoretical_results = self.estimate_yield(
            target_protein_content, efficiency_factor=1.0
        )
        theoretical_yield = theoretical_results["theoretical_yield"]

        # Calculate efficiency metrics
        process_efficiency = (actual_yield / theoretical_yield) * 100
        yield_gap = theoretical_yield - actual_yield
        improvement_potential = 100 - process_efficiency

        return {
            "process_efficiency": process_efficiency,
            "yield_gap": yield_gap,
            "improvement_potential": improvement_potential,
        }
