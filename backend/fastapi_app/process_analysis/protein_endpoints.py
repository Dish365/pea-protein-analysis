from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Union
import logging

from backend.fastapi_app.models.protein_analysis import (
    ProteinRecoveryInput,
    SeparationEfficiencyInput,
    ParticleSizeInput,
    ProteinAnalysisResponse,
)
from analytics.protein_analysis.recovery import ProteinRecoveryCalculator
from analytics.protein_analysis.separation import SeparationEfficiencyAnalyzer
from analytics.protein_analysis.particle_size import ParticleSizeAnalyzer

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/protein-analysis",
    tags=["protein-analysis"],
    responses={
        404: {"description": "Analysis not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal calculation error"},
    },
)


@router.post("/recovery/", response_model=Dict[str, float])
async def calculate_protein_recovery(input_data: ProteinRecoveryInput):
    """
    Calculate protein recovery metrics including recovery rate, loss, and yield estimates.
    
    Endpoint combines recovery calculation with yield estimation for comprehensive analysis.
    """
    logger.info(f"Processing protein recovery calculation with input: {input_data}")
    try:
        calculator = ProteinRecoveryCalculator(input_data.initial_protein_content)
        logger.debug(f"Initialized ProteinRecoveryCalculator with initial content: {input_data.initial_protein_content}%")

        # Calculate recovery metrics
        logger.debug("Calculating recovery metrics...")
        recovery_results = calculator.calculate_recovery(
            output_mass=input_data.output_mass,
            input_mass=input_data.input_mass,
            output_protein_content=input_data.output_protein_content,
        )
        logger.debug(f"Recovery results: {recovery_results}")

        # Estimate yield based on target protein content
        logger.debug("Estimating yield metrics...")
        yield_results = calculator.estimate_yield(
            target_protein_content=input_data.output_protein_content
        )
        logger.debug(f"Yield results: {yield_results}")

        # Combine results
        final_results = {**recovery_results, **yield_results}
        logger.info(f"Successfully calculated protein recovery metrics: {final_results}")
        return final_results

    except ValueError as ve:
        logger.error(f"Validation error in protein recovery calculation: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in protein recovery calculation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Recovery calculation failed: {str(e)}")


@router.post("/separation/", response_model=Dict[str, Union[float, Dict[str, float]]])
async def analyze_separation_efficiency(input_data: SeparationEfficiencyInput):
    """
    Analyze separation efficiency and process performance metrics.
    
    Combines basic efficiency calculations with process performance analysis when process data is provided.
    """
    logger.info(f"Processing separation efficiency analysis with input: {input_data}")
    try:
        analyzer = SeparationEfficiencyAnalyzer()
        logger.debug("Initialized SeparationEfficiencyAnalyzer")

        # Calculate basic efficiency metrics
        logger.debug("Calculating basic efficiency metrics...")
        efficiency_results = analyzer.calculate_efficiency(
            feed_composition=input_data.feed_composition,
            product_composition=input_data.product_composition,
            mass_flow=input_data.mass_flow,
        )
        logger.debug(f"Basic efficiency results: {efficiency_results}")

        # Ensure component_recoveries is a dictionary of floats
        if "component_recoveries" in efficiency_results:
            efficiency_results["component_recoveries"] = {
                k: float(v) for k, v in efficiency_results["component_recoveries"].items()
            }
            logger.debug(f"Processed component recoveries: {efficiency_results['component_recoveries']}")

        # If process data is provided, analyze overall performance
        if input_data.process_data and input_data.target_purity:
            logger.debug("Analyzing process performance with additional data...")
            performance_results = analyzer.analyze_process_performance(
                process_data=input_data.process_data,
                target_purity=input_data.target_purity,
            )
            efficiency_results.update(performance_results)
            logger.debug(f"Performance analysis results: {performance_results}")

            # Calculate stage contributions if multiple stages
            if len(input_data.process_data) > 1:
                logger.debug("Calculating multi-stage contributions...")
                stage_results = analyzer.calculate_stage_contributions(
                    process_data=input_data.process_data
                )
                efficiency_results["stage_analysis"] = stage_results
                logger.debug(f"Stage analysis results: {stage_results}")

        logger.info(f"Successfully completed separation efficiency analysis: {efficiency_results}")
        return efficiency_results

    except ValueError as ve:
        logger.error(f"Validation error in separation efficiency analysis: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in separation efficiency analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Separation analysis failed: {str(e)}")


@router.post("/particle-size/", response_model=Dict[str, float])
async def analyze_particle_size(input_data: ParticleSizeInput):
    """
    Analyze particle size distribution and related quality metrics.
    
    Uses Rust for computationally intensive calculations.
    """
    logger.info(f"Processing particle size analysis with input: {input_data}")
    try:
        analyzer = ParticleSizeAnalyzer()
        logger.debug("Initialized ParticleSizeAnalyzer")

        # Analyze size distribution using Rust
        logger.debug("Analyzing particle size distribution using Rust...")
        distribution_results = analyzer.analyze_distribution(
            particle_sizes=input_data.particle_sizes,
            weights=input_data.weights,
        )
        logger.debug(f"Distribution analysis results: {distribution_results}")

        # Evaluate quality if target ranges provided
        if input_data.target_ranges:
            logger.debug(f"Evaluating size quality with target ranges: {input_data.target_ranges}")
            quality_results = analyzer.evaluate_size_quality(
                distribution_params=distribution_results,
                target_ranges=input_data.target_ranges,
            )
            distribution_results.update(quality_results)
            logger.debug(f"Quality evaluation results: {quality_results}")

        # Calculate surface area if density provided
        if input_data.density:
            logger.debug(f"Calculating surface area with density: {input_data.density}")
            surface_results = analyzer.calculate_surface_area(
                particle_sizes=input_data.particle_sizes,
                density=input_data.density,
                weights=input_data.weights,
            )
            distribution_results.update(surface_results)
            logger.debug(f"Surface area calculation results: {surface_results}")

        logger.info(f"Successfully completed particle size analysis: {distribution_results}")
        return distribution_results

    except ValueError as ve:
        logger.error(f"Validation error in particle size analysis: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in particle size analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Particle size analysis failed: {str(e)}")


@router.post("/complete-analysis/", response_model=ProteinAnalysisResponse)
async def perform_complete_analysis(
    recovery_input: ProteinRecoveryInput,
    separation_input: SeparationEfficiencyInput,
    particle_input: ParticleSizeInput,
):
    """
    Perform comprehensive protein analysis combining all metrics.
    
    Executes all three analyses (recovery, separation, particle size) and combines results
    into a single comprehensive response.
    """
    logger.info("Starting complete protein analysis")
    try:
        # Get recovery metrics
        logger.debug("Processing recovery analysis...")
        recovery_metrics = await calculate_protein_recovery(recovery_input)
        logger.debug(f"Recovery metrics: {recovery_metrics}")

        # Get separation metrics
        logger.debug("Processing separation analysis...")
        separation_metrics = await analyze_separation_efficiency(separation_input)
        logger.debug(f"Separation metrics: {separation_metrics}")

        # Get particle metrics
        logger.debug("Processing particle size analysis...")
        particle_metrics = await analyze_particle_size(particle_input)
        logger.debug(f"Particle metrics: {particle_metrics}")

        # Extract process performance metrics if available
        process_performance = None
        if "cumulative_efficiency" in separation_metrics:
            logger.debug("Extracting process performance metrics...")
            process_performance = {
                "cumulative_efficiency": separation_metrics["cumulative_efficiency"],
                "average_step_efficiency": separation_metrics.get("average_step_efficiency"),
                "purity_achievement": separation_metrics.get("purity_achievement"),
            }
            logger.debug(f"Process performance metrics: {process_performance}")

        response = ProteinAnalysisResponse(
            recovery_metrics=recovery_metrics,
            separation_metrics=separation_metrics,
            particle_metrics=particle_metrics,
            process_performance=process_performance,
        )
        logger.info("Successfully completed comprehensive protein analysis")
        return response

    except HTTPException:
        logger.error("HTTP exception occurred during complete analysis", exc_info=True)
        raise  # Re-raise HTTP exceptions as is
    except Exception as e:
        logger.error(f"Unexpected error in complete analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Complete analysis failed: {str(e)}")
