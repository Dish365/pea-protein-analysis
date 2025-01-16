from fastapi import APIRouter, HTTPException
from typing import Dict, List

from ..models.protein_analysis import (
    ProteinRecoveryInput,
    SeparationEfficiencyInput,
    ParticleSizeInput,
    ProteinAnalysisResponse,
)
from analytics.protein_analysis.recovery import ProteinRecoveryCalculator
from analytics.protein_analysis.separation import SeparationEfficiencyAnalyzer
from analytics.protein_analysis.particle_size import ParticleSizeAnalyzer

router = APIRouter(prefix="/process/technical", tags=["protein-analysis"])


@router.post("/protein-recovery/", response_model=Dict[str, float])
async def calculate_protein_recovery(input_data: ProteinRecoveryInput):
    """Calculate protein recovery rate and related metrics."""
    try:
        calculator = ProteinRecoveryCalculator(input_data.initial_protein_content)

        # Calculate recovery metrics
        recovery_results = calculator.calculate_recovery(
            output_mass=input_data.output_mass,
            input_mass=input_data.input_mass,
            output_protein_content=input_data.output_protein_content,
        )

        # Estimate yield
        yield_results = calculator.estimate_yield(
            target_protein_content=input_data.output_protein_content
        )

        return {**recovery_results, **yield_results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/separation-efficiency/", response_model=Dict[str, float])
async def calculate_separation_efficiency(input_data: SeparationEfficiencyInput):
    """Calculate separation efficiency and process performance metrics."""
    try:
        analyzer = SeparationEfficiencyAnalyzer()

        # Calculate basic efficiency metrics
        efficiency_results = analyzer.calculate_efficiency(
            feed_composition=input_data.feed_composition,
            product_composition=input_data.product_composition,
            mass_flow=input_data.mass_flow,
        )

        # If process data is provided, analyze overall performance
        if input_data.process_data:
            performance_results = analyzer.analyze_process_performance(
                process_data=input_data.process_data,
                target_purity=input_data.target_purity,
            )
            efficiency_results.update(performance_results)

        return efficiency_results
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/particle-size/", response_model=Dict[str, float])
async def analyze_particle_size(input_data: ParticleSizeInput):
    """Analyze particle size distribution and quality metrics."""
    try:
        analyzer = ParticleSizeAnalyzer()

        # Analyze distribution
        distribution_results = analyzer.analyze_distribution(
            particle_sizes=input_data.particle_sizes, weights=input_data.weights
        )

        results = distribution_results.copy()

        # Calculate quality metrics if target ranges provided
        if input_data.target_ranges:
            quality_results = analyzer.evaluate_size_quality(
                distribution_params=distribution_results,
                target_ranges=input_data.target_ranges,
            )
            results.update(quality_results)

        # Calculate surface area if density provided
        if input_data.density:
            surface_results = analyzer.calculate_surface_area(
                particle_sizes=input_data.particle_sizes,
                density=input_data.density,
                weights=input_data.weights,
            )
            results.update(surface_results)

        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete-analysis/", response_model=ProteinAnalysisResponse)
async def perform_complete_analysis(
    recovery_input: ProteinRecoveryInput,
    separation_input: SeparationEfficiencyInput,
    particle_input: ParticleSizeInput,
):
    """Perform comprehensive protein analysis including all metrics."""
    try:
        # Get recovery metrics
        recovery_metrics = await calculate_protein_recovery(recovery_input)

        # Get separation metrics
        separation_metrics = await calculate_separation_efficiency(separation_input)

        # Get particle metrics
        particle_metrics = await analyze_particle_size(particle_input)

        # Get process performance from separation metrics
        process_performance = (
            {
                "cumulative_efficiency": separation_metrics.get(
                    "cumulative_efficiency", 0.0
                )
            }
            if "cumulative_efficiency" in separation_metrics
            else None
        )

        return ProteinAnalysisResponse(
            recovery_metrics=recovery_metrics,
            separation_metrics=separation_metrics,
            particle_metrics=particle_metrics,
            process_performance=process_performance,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {str(e)}")
