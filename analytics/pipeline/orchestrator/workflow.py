from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import logging
from ..integrator.technical import TechnicalIntegrator
from ..integrator.economic import EconomicIntegrator
from ..integrator.environmental import EnvironmentalIntegrator
from .error_handling import handle_error, retry_operation

logger = logging.getLogger(__name__)


class AnalysisWorkflow:
    def __init__(self):
        self.technical = TechnicalIntegrator()
        self.economic = EconomicIntegrator()
        self.environmental = EnvironmentalIntegrator()

    async def execute_workflow(
        self, input_data: Dict[str, Any], workflow_type: str, max_retries: int = 3
    ) -> Dict[str, Any]:
        """Execute analysis workflow with error handling and retries"""
        try:
            if workflow_type == "technical":
                return await self._run_technical_workflow(input_data, max_retries)
            elif workflow_type == "economic":
                return await self._run_economic_workflow(input_data, max_retries)
            elif workflow_type == "environmental":
                return await self._run_environmental_workflow(input_data, max_retries)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return handle_error(e)

    async def _run_technical_workflow(
        self, input_data: Dict[str, Any], max_retries: int
    ) -> Dict[str, Any]:
        """Execute technical analysis workflow"""
        results = {}

        # Protein recovery analysis
        protein_data = input_data.get("protein_data", {})
        results["protein_recovery"] = await retry_operation(
            lambda: self.technical.analyze_protein_recovery(
                protein_data.get("yield", 0),
                protein_data.get("content", 0),
                protein_data.get("efficiency", 0),
            ),
            max_retries=max_retries,
        )

        # Particle distribution analysis
        particle_data = input_data.get("particle_data", [])
        results["particle_distribution"] = await retry_operation(
            lambda: self.technical.analyze_particle_distribution(particle_data),
            max_retries=max_retries,
        )

        return results

    async def _run_economic_workflow(
        self, input_data: Dict[str, Any], max_retries: int
    ) -> Dict[str, Any]:
        """Execute economic analysis workflow"""
        results = {}

        # Monte Carlo analysis
        economic_data = input_data.get("economic_data", {})
        results["monte_carlo"] = await retry_operation(
            lambda: self.economic.run_monte_carlo_analysis(
                economic_data.get("values", []),
                economic_data.get("iterations", 1000),
                economic_data.get("uncertainty", 0.1),
            ),
            max_retries=max_retries,
        )

        # Sensitivity analysis
        sensitivity_data = input_data.get("sensitivity_data", {})
        results["sensitivity"] = await retry_operation(
            lambda: self.economic.analyze_economic_sensitivity(
                sensitivity_data.get("values", []),
                sensitivity_data.get("parameters", []),
            ),
            max_retries=max_retries,
        )

        return results

    async def _run_environmental_workflow(
        self, input_data: Dict[str, Any], max_retries: int
    ) -> Dict[str, Any]:
        """Execute environmental analysis workflow"""
        results = {}

        # Impact matrix calculation
        env_data = input_data.get("environmental_data", {})
        results["impact_matrix"] = await retry_operation(
            lambda: self.environmental.calculate_impact_matrix(
                env_data.get("process_matrix", []), env_data.get("impact_factors", [])
            ),
            max_retries=max_retries,
        )

        # Allocation factors calculation
        allocation_data = input_data.get("allocation_data", {})
        results["allocation_factors"] = await retry_operation(
            lambda: self.environmental.calculate_allocation_factors(
                allocation_data.get("correlation_matrix", [])
            ),
            max_retries=max_retries,
        )

        # Impact normalization
        normalization_data = input_data.get("normalization_data", {})
        results["normalized_impacts"] = await retry_operation(
            lambda: self.environmental.normalize_impacts(
                normalization_data.get("impacts", []),
                normalization_data.get("reference_values", []),
            ),
            max_retries=max_retries,
        )

        return results
