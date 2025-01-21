import numpy as np
from typing import Dict, List, Optional


class SeparationEfficiencyAnalyzer:
    """
    Analyze separation efficiency metrics in protein fractionation processes.

    This class implements methods for analyzing separation efficiency and process
    performance in protein fractionation, including:
    - Component separation factors
    - Protein enrichment calculation
    - Process efficiency analysis
    - Multi-stage separation performance

    Mathematical Background:
    ----------------------
    1. Separation Factor (α):
       α = (Cp₂/Cp₁)/(Cs₂/Cs₁)
       where:
       - Cp₂ = Protein concentration in product
       - Cp₁ = Protein concentration in feed
       - Cs₂ = Secondary component concentration in product
       - Cs₁ = Secondary component concentration in feed

    2. Protein Enrichment (E):
       E = Cp₂ - Cp₁
       where:
       - Cp₂ = Final protein concentration
       - Cp₁ = Initial protein concentration

    3. Separation Efficiency (η):
       η = (Mp₂ * Cp₂)/(Mp₁ * Cp₁) * 100%
       where:
       - Mp₂ = Product mass flow
       - Mp₁ = Feed mass flow
       - Cp₂ = Product protein concentration
       - Cp₁ = Feed protein concentration

    4. Overall Process Performance:
       ηₒᵥ = η₁ * η₂ * ... * ηₙ
       where:
       - ηᵢ = Efficiency of stage i
    """

    def _validate_composition(self, composition: Dict[str, float]) -> None:
        """
        Validate composition percentages sum to approximately 100%.

        Args:
            composition: Dict of component names and their percentages

        Raises:
            ValueError: If percentages don't sum to approximately 100%
        """
        total = sum(composition.values())
        if not (99.5 <= total <= 100.5):  # Allow small rounding errors
            raise ValueError(f"Composition percentages must sum to 100% (got {total}%)")

    def _validate_mass_flows(self, mass_flow: Dict[str, float]) -> None:
        """
        Validate mass flow values.

        Args:
            mass_flow: Dict with input and output mass flows

        Raises:
            ValueError: If mass flows violate physical constraints
        """
        if mass_flow["output"] > mass_flow["input"]:
            raise ValueError("Output mass cannot exceed input mass")
        if any(flow <= 0 for flow in mass_flow.values()):
            raise ValueError("Mass flows must be positive")

    def _validate_component_match(self, feed_composition: Dict[str, float],
                                product_composition: Dict[str, float]) -> None:
        """
        Validate that feed and product have matching components.

        Args:
            feed_composition: Dict of feed components and percentages
            product_composition: Dict of product components and percentages

        Raises:
            ValueError: If component sets don't match
        """
        if set(feed_composition.keys()) != set(product_composition.keys()):
            raise ValueError("Feed and product compositions must have the same components")

    def calculate_efficiency(
        self,
        feed_composition: Dict[str, float],
        product_composition: Dict[str, float],
        mass_flow: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Calculate separation efficiency metrics for a single stage.

        Algorithm:
        1. Calculate protein separation factor
        2. Calculate enrichment
        3. Calculate mass-based efficiency
        4. Calculate component recoveries

        Mathematical Details:
        -------------------
        1. Component Recovery (Rc):
           Rc = (M₂ * C₂)/(M₁ * C₁) * 100%
           where:
           - M₂ = Output mass flow
           - C₂ = Output concentration
           - M₁ = Input mass flow
           - C₁ = Input concentration

        2. Protein Enrichment:
           E = C₂ - C₁

        Args:
            feed_composition: Dict with component percentages in feed
            product_composition: Dict with component percentages in product
            mass_flow: Dict with input and output mass flows

        Returns:
            Dict containing:
            - separation_factor: Protein/non-protein separation factor
            - protein_enrichment: Absolute increase in protein content
            - separation_efficiency: Overall separation efficiency
            - component_recoveries: Recovery rates for each component

        Raises:
            ValueError: If compositions don't contain required components or violate constraints
        """
        # Validate inputs
        if "protein" not in feed_composition or "protein" not in product_composition:
            raise ValueError("Compositions must include protein content")
        if "input" not in mass_flow or "output" not in mass_flow:
            raise ValueError("Mass flow must include input and output")

        # Additional validations
        self._validate_composition(feed_composition)
        self._validate_composition(product_composition)
        self._validate_mass_flows(mass_flow)
        self._validate_component_match(feed_composition, product_composition)

        # Extract flow rates
        input_flow = mass_flow["input"]
        output_flow = mass_flow["output"]

        # Calculate protein enrichment
        protein_enrichment = (
            product_composition["protein"] - feed_composition["protein"]
        )

        # Calculate separation efficiency with zero check
        if feed_composition["protein"] <= 0:
            raise ValueError("Feed protein content must be greater than 0")
        
        separation_efficiency = (
            (output_flow * product_composition["protein"])
            / (input_flow * feed_composition["protein"])
        ) * 100

        # Calculate component recoveries with zero handling
        component_recoveries = {}
        for component in feed_composition:
            if component in product_composition:
                if feed_composition[component] <= 0:
                    if product_composition[component] <= 0:
                        # Both feed and product are zero - perfect recovery
                        component_recoveries[component] = 100.0
                    else:
                        # Component appears in product but not in feed - invalid
                        raise ValueError(
                            f"Invalid mass balance: {component} appears in product but not in feed"
                        )
                else:
                    recovery = (
                        (output_flow * product_composition[component])
                        / (input_flow * feed_composition[component])
                    ) * 100
                    component_recoveries[component] = recovery

        # Calculate separation factor with zero handling
        protein_ratio = product_composition["protein"] / feed_composition["protein"]
        non_protein_feed = 100 - feed_composition["protein"]
        non_protein_product = 100 - product_composition["protein"]
        
        if non_protein_feed <= 0:
            separation_factor = float("inf")
        else:
            non_protein_ratio = non_protein_product / non_protein_feed
            if non_protein_ratio <= 0:
                separation_factor = float("inf")
            else:
                separation_factor = protein_ratio / non_protein_ratio

        return {
            "separation_factor": separation_factor,
            "protein_enrichment": protein_enrichment,
            "separation_efficiency": separation_efficiency,
            "component_recoveries": component_recoveries,
        }

    def analyze_process_performance(
        self, process_data: List[Dict], target_purity: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Analyze overall process performance across multiple separation stages.

        Mathematical Background:
        ----------------------
        1. Cumulative Efficiency:
           ηc = Π(ηᵢ)
           where ηᵢ is the efficiency of stage i

        2. Average Stage Efficiency:
           ηₐᵥg = (ηc)^(1/n)
           where n is the number of stages

        3. Purity Achievement:
           PA = (Cf/Ct) * 100%
           where:
           - Cf = Final protein concentration
           - Ct = Target protein concentration

        Args:
            process_data: List of dicts containing step-wise process data
            target_purity: Target protein purity percentage

        Returns:
            Dict containing:
            - cumulative_efficiency: Overall process efficiency
            - cumulative_enrichment: Total protein enrichment
            - average_step_efficiency: Geometric mean of step efficiencies
            - purity_achievement: Progress toward target purity (if specified)
        """
        if not process_data:
            raise ValueError("Process data cannot be empty")

        cumulative_efficiency = 100.0
        cumulative_enrichment = 0.0
        step_efficiencies = []

        for step in process_data:
            # Calculate step efficiency
            step_results = self.calculate_efficiency(
                step["feed"], step["product"], step["mass_flow"]
            )

            # Update cumulative metrics
            cumulative_efficiency *= step_results["separation_efficiency"] / 100
            cumulative_enrichment += step_results["protein_enrichment"]
            step_efficiencies.append(step_results["separation_efficiency"])

        # Calculate average step efficiency
        n_steps = len(process_data)
        average_step_efficiency = cumulative_efficiency ** (1 / n_steps)

        results = {
            "cumulative_efficiency": cumulative_efficiency,
            "cumulative_enrichment": cumulative_enrichment,
            "average_step_efficiency": average_step_efficiency,
        }

        # Calculate purity achievement if target specified
        if target_purity is not None:
            if target_purity <= 0:
                raise ValueError("Target purity must be positive")
            final_purity = process_data[-1]["product"]["protein"]
            purity_achievement = (final_purity / target_purity) * 100
            results["purity_achievement"] = min(purity_achievement, 100.0)  # Cap at 100%

        return results

    def calculate_stage_contributions(
        self, process_data: List[Dict]
    ) -> Dict[str, List[float]]:
        """
        Calculate individual stage contributions to overall separation.

        Mathematical Details:
        -------------------
        1. Stage Contribution (Cs):
           Cs = (ΔCᵢ/ΔCₜ) * 100%
           where:
           - ΔCᵢ = Protein enrichment in stage i
           - ΔCₜ = Total protein enrichment

        2. Relative Efficiency (Er):
           Er = ηᵢ/ηₐᵥg
           where:
           - ηᵢ = Stage efficiency
           - ηₐᵥg = Average stage efficiency

        Args:
            process_data: List of dicts containing step-wise process data

        Returns:
            Dict containing:
            - enrichment_contributions: Percentage contribution to total enrichment
            - efficiency_ratios: Ratio of stage efficiency to average
            - bottleneck_scores: Relative process bottleneck indicators
        """
        if not process_data:
            raise ValueError("Process data cannot be empty")

        enrichment_contributions = []
        efficiency_ratios = []
        total_enrichment = 0.0
        efficiencies = []

        # First pass: collect enrichments and efficiencies
        for step in process_data:
            results = self.calculate_efficiency(
                step["feed"], step["product"], step["mass_flow"]
            )
            enrichment = results["protein_enrichment"]
            efficiency = results["separation_efficiency"]

            total_enrichment += abs(enrichment)
            efficiencies.append(efficiency)

        # Calculate average efficiency
        avg_efficiency = np.mean(efficiencies) if efficiencies else 0.0

        # Second pass: calculate contributions and ratios
        for step in process_data:
            results = self.calculate_efficiency(
                step["feed"], step["product"], step["mass_flow"]
            )

            # Calculate enrichment contribution
            contribution = (
                abs(results["protein_enrichment"]) / total_enrichment * 100
                if total_enrichment > 0
                else 0.0
            )
            enrichment_contributions.append(contribution)

            # Calculate efficiency ratio
            ratio = (
                results["separation_efficiency"] / avg_efficiency
                if avg_efficiency > 0
                else 0.0
            )
            efficiency_ratios.append(ratio)

        # Calculate bottleneck scores
        # Lower score indicates potential bottleneck
        bottleneck_scores = [
            ratio * contribution / 100
            for ratio, contribution in zip(efficiency_ratios, enrichment_contributions)
        ]

        return {
            "enrichment_contributions": enrichment_contributions,
            "efficiency_ratios": efficiency_ratios,
            "bottleneck_scores": bottleneck_scores,
        }
