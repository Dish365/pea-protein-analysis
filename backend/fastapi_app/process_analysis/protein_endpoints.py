from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Union
import logging
from functools import lru_cache
import hashlib
import json

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

# Initialize analyzers
particle_analyzer = ParticleSizeAnalyzer()

@lru_cache(maxsize=1000)
def _cached_particle_analysis(cache_key: str, **kwargs) -> Dict:
    """Cached version of particle size analysis"""
    return particle_analyzer.process_sample(**kwargs)

def _generate_cache_key(input_data: ParticleSizeInput) -> str:
    """Generate cache key from input data"""
    # Convert input data to dictionary, excluding None values
    data_dict = {k: v for k, v in input_data.dict().items() if v is not None}
    # Convert to JSON string and hash
    return hashlib.sha256(json.dumps(data_dict, sort_keys=True).encode()).hexdigest()

@router.post("/recovery/", response_model=Dict[str, float])
async def calculate_protein_recovery(input_data: ProteinRecoveryInput):
    """
    Calculate protein recovery metrics including recovery rate, loss, and yield estimates.
    
    Endpoint combines recovery calculation with yield estimation for comprehensive analysis.
    The yield estimation uses the output_protein_content as the target to estimate
    theoretical maximum yield and expected yield with typical process efficiency.
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

        # Calculate process efficiency based on actual vs theoretical yield
        actual_yield = (input_data.output_mass * input_data.output_protein_content) / (input_data.input_mass * input_data.initial_protein_content) * 100
        process_efficiency = calculator.analyze_process_efficiency(
            actual_yield=actual_yield,
            target_protein_content=input_data.output_protein_content
        )
        logger.debug(f"Process efficiency results: {process_efficiency}")

        # Combine all results
        final_results = {
            **recovery_results,
            **process_efficiency
        }
        logger.info(f"Successfully calculated protein recovery metrics: {final_results}")
        return final_results

    except ValueError as ve:
        logger.error(f"Validation error in protein recovery calculation: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in protein recovery calculation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Recovery calculation failed: {str(e)}")


@lru_cache(maxsize=1000)
def _cached_separation_analysis(cache_key: str, feed_composition_str: str, product_composition_str: str, mass_flow_str: str) -> Dict:
    """Cached version of separation efficiency analysis"""
    analyzer = SeparationEfficiencyAnalyzer()
    # Convert string representations back to dictionaries
    feed_composition = json.loads(feed_composition_str)
    product_composition = json.loads(product_composition_str)
    mass_flow = json.loads(mass_flow_str)
    return analyzer.calculate_efficiency(
        feed_composition=feed_composition,
        product_composition=product_composition,
        mass_flow=mass_flow
    )

def _generate_separation_cache_key(input_data: SeparationEfficiencyInput) -> tuple[str, str, str, str]:
    """Generate cache key components from separation input data"""
    # Convert dictionaries to sorted JSON strings for consistent hashing
    feed_str = json.dumps(dict(sorted(input_data.feed_composition.items())))
    product_str = json.dumps(dict(sorted(input_data.product_composition.items())))
    mass_flow_str = json.dumps(dict(sorted(input_data.mass_flow.items())))
    # Generate a hash for the combined data
    combined = feed_str + product_str + mass_flow_str
    cache_key = hashlib.sha256(combined.encode()).hexdigest()
    return cache_key, feed_str, product_str, mass_flow_str

@router.post("/separation/", response_model=Dict[str, Union[float, Dict[str, float]]])
async def analyze_separation_efficiency(
    input_data: SeparationEfficiencyInput,
    background_tasks: BackgroundTasks
):
    """
    Analyze separation efficiency and process performance metrics.
    
    Combines basic efficiency calculations with process performance analysis when process data is provided.
    Implements caching for repeated calculations and background tasks for cleanup.
    """
    logger.info(f"Processing separation efficiency analysis with input: {input_data}")
    try:
        # Generate cache key components
        cache_key, feed_str, product_str, mass_flow_str = _generate_separation_cache_key(input_data)
        logger.debug(f"Generated cache key: {cache_key}")

        # Try to get cached results for basic efficiency
        try:
            efficiency_results = _cached_separation_analysis(
                cache_key,
                feed_str,
                product_str,
                mass_flow_str
            )
            logger.debug("Retrieved basic efficiency results from cache")
        except Exception as cache_error:
            logger.warning(f"Cache retrieval failed: {str(cache_error)}")
            # Fallback to direct calculation
            analyzer = SeparationEfficiencyAnalyzer()
            efficiency_results = analyzer.calculate_efficiency(
                feed_composition=input_data.feed_composition,
                product_composition=input_data.product_composition,
                mass_flow=input_data.mass_flow,
            )
            logger.debug("Calculated basic efficiency results directly")

        # Ensure component_recoveries contains floats and maintains input order
        if "component_recoveries" in efficiency_results:
            # Get the order of components from input feed composition
            component_order = list(input_data.feed_composition.keys())
            efficiency_results["component_recoveries"] = {
                k: float(efficiency_results["component_recoveries"][k])
                for k in component_order
                if k in efficiency_results["component_recoveries"]
            }
            logger.debug(f"Processed component recoveries: {efficiency_results['component_recoveries']}")

        # If process data is provided, analyze overall performance
        if input_data.process_data and input_data.target_purity:
            logger.debug("Analyzing process performance with additional data...")
            try:
                analyzer = SeparationEfficiencyAnalyzer()
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
            except ValueError as ve:
                logger.error(f"Process performance analysis failed: {str(ve)}")
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": "Process performance analysis failed",
                        "message": str(ve),
                        "type": "ValueError"
                    }
                )
            except Exception as e:
                logger.error(f"Unexpected error in process performance analysis: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Process performance analysis failed",
                        "message": str(e),
                        "type": type(e).__name__
                    }
                )

        # Add cleanup task
        background_tasks.add_task(logger.info, f"Completed separation analysis for key: {cache_key}")

        logger.info("Successfully completed separation efficiency analysis")
        return efficiency_results

    except ValueError as ve:
        logger.error(f"Validation error in separation efficiency analysis: {str(ve)}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Validation error",
                "message": str(ve),
                "type": "ValueError"
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in separation efficiency analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Separation analysis failed",
                "message": str(e),
                "type": type(e).__name__
            }
        )


@router.post("/particle-size/", response_model=Dict[str, Union[float, Dict]])
async def analyze_particle_size(
    input_data: ParticleSizeInput,
    background_tasks: BackgroundTasks
):
    """
    Analyze particle size distribution and related quality metrics.
    
    Includes moisture content tracking and validation through processing stages.
    Uses Rust for computationally intensive calculations.
    Implements caching for repeated calculations.
    """
    logger.info(f"Processing particle size analysis with input: {input_data}")
    try:
        # Generate cache key
        cache_key = _generate_cache_key(input_data)
        logger.debug(f"Generated cache key: {cache_key}")

        # Prepare analysis parameters
        analysis_params = {
            "particle_data": {
                "sizes": input_data.particle_sizes,
                "weights": input_data.weights,
                "percentiles": None,  # Will be calculated
                "density": input_data.density,
                "initial_moisture": input_data.initial_moisture,
                "final_moisture": input_data.final_moisture
            },
            "treatment_type": input_data.treatment_type
        }

        # Try to get cached results
        try:
            distribution_results = _cached_particle_analysis(cache_key, **analysis_params)
            logger.debug("Retrieved results from cache")
        except Exception as cache_error:
            logger.warning(f"Cache retrieval failed: {str(cache_error)}")
            # Fallback to direct calculation
            distribution_results = particle_analyzer.process_sample(**analysis_params)
            logger.debug("Calculated results directly")

        # Evaluate quality if target ranges provided
        if input_data.target_ranges:
            logger.debug(f"Evaluating size quality with target ranges: {input_data.target_ranges}")
            try:
                quality_results = particle_analyzer.evaluate_size_quality(
                    distribution_params=distribution_results,
                    target_ranges=input_data.target_ranges,
                )
                distribution_results.update(quality_results)
                logger.debug(f"Quality evaluation results: {quality_results}")
            except Exception as quality_error:
                logger.error(f"Quality evaluation failed: {str(quality_error)}")
                raise ValueError(f"Quality evaluation failed: {str(quality_error)}")

        # Calculate surface area if density provided
        if input_data.density:
            logger.debug(f"Calculating surface area with density: {input_data.density}")
            try:
                surface_results = particle_analyzer.calculate_surface_area(
                    particle_sizes=input_data.particle_sizes,
                    density=input_data.density,
                    weights=input_data.weights,
                )
                distribution_results.update(surface_results)
                logger.debug(f"Surface area calculation results: {surface_results}")
            except Exception as surface_error:
                logger.error(f"Surface area calculation failed: {str(surface_error)}")
                raise ValueError(f"Surface area calculation failed: {str(surface_error)}")

        # Add cleanup task to background tasks
        background_tasks.add_task(logger.info, f"Completed particle size analysis for key: {cache_key}")

        logger.info("Successfully completed particle size analysis with moisture tracking")
        return distribution_results

    except ValueError as ve:
        logger.error(f"Validation error in particle size analysis: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in particle size analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Particle size analysis failed",
                "message": str(e),
                "type": type(e).__name__
            }
        )


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
