from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Union
import logging
from functools import lru_cache
import hashlib
import json

# Get logger from the main app's hierarchy
logger = logging.getLogger('backend.fastapi_app.process_analysis.protein_endpoints')

from backend.fastapi_app.models.protein_analysis import (
    ProteinRecoveryInput,
    SeparationEfficiencyInput,
    ParticleSizeInput,
    ProteinAnalysisResponse,
    ProcessType,
)
from analytics.protein_analysis.recovery import ProteinRecoveryCalculator
from analytics.protein_analysis.separation import SeparationEfficiencyAnalyzer
from analytics.protein_analysis.particle_size import ParticleSizeAnalyzer

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
logger.info("ParticleSizeAnalyzer initialized")

@lru_cache(maxsize=1000)
def _cached_particle_analysis(cache_key: str, particle_data: Dict, treatment_type: Optional[ProcessType] = None) -> Dict:
    """Cached version of particle size analysis"""
    logger.debug(f"Attempting cached particle analysis with key: {cache_key}")
    logger.debug(f"Particle data: {particle_data}")
    
    try:
        result = particle_analyzer.process_sample(
            particle_data=particle_data,
            treatment_type=treatment_type
        )
        logger.debug(f"Cached particle analysis successful")
        return result
    except Exception as e:
        logger.error(f"Error in cached particle analysis: {str(e)}", exc_info=True)
        raise

def _generate_cache_key(input_data: ParticleSizeInput) -> str:
    """Generate cache key from input data"""
    logger.debug("Generating cache key for particle analysis")
    try:
        # Convert input data to a tuple of key components
        key_components = (
            tuple(input_data.particle_sizes),
            tuple(input_data.weights) if input_data.weights else None,
            input_data.density,
            input_data.initial_moisture,
            input_data.final_moisture,
            input_data.treatment_type.value if input_data.treatment_type else None
        )
        # Convert to string and hash
        cache_key = hashlib.sha256(str(key_components).encode()).hexdigest()
        logger.debug(f"Generated cache key: {cache_key}")
        return cache_key
    except Exception as e:
        logger.error(f"Error generating cache key: {str(e)}", exc_info=True)
        raise

@router.post("/recovery/", response_model=Dict[str, float])
async def calculate_protein_recovery(input_data: ProteinRecoveryInput):
    """Calculate protein recovery metrics"""
    logger.info("Processing protein recovery calculation")
    logger.debug(f"Recovery input data: {input_data.dict()}")
    
    try:
        calculator = ProteinRecoveryCalculator(input_data.initial_protein_content)
        logger.debug(f"ProteinRecoveryCalculator initialized with initial content: {input_data.initial_protein_content}%")

        # Calculate recovery metrics
        logger.debug("Calculating recovery metrics...")
        recovery_results = calculator.calculate_recovery(
            output_mass=input_data.output_mass,
            input_mass=input_data.input_mass,
            output_protein_content=input_data.output_protein_content,
        )
        logger.debug(f"Recovery results: {recovery_results}")

        # Calculate process efficiency
        actual_yield = (input_data.output_mass * input_data.output_protein_content) / (input_data.input_mass * input_data.initial_protein_content) * 100
        logger.debug(f"Calculated actual yield: {actual_yield}%")
        
        process_efficiency = calculator.analyze_process_efficiency(
            actual_yield=actual_yield,
            target_protein_content=input_data.output_protein_content
        )
        logger.debug(f"Process efficiency results: {process_efficiency}")

        # Combine results
        final_results = {
            **recovery_results,
            **process_efficiency
        }
        logger.info(f"Successfully calculated protein recovery metrics")
        logger.debug(f"Final recovery results: {final_results}")
        return final_results

    except ValueError as ve:
        logger.error(f"Validation error in protein recovery calculation: {str(ve)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in protein recovery calculation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Recovery calculation failed: {str(e)}")

@router.post("/separation/", response_model=Dict[str, Union[float, Dict[str, float]]])
async def analyze_separation_efficiency(
    input_data: SeparationEfficiencyInput,
    background_tasks: BackgroundTasks
):
    """Analyze separation efficiency"""
    logger.info("Processing separation efficiency analysis")
    logger.debug(f"Separation input data: {input_data.dict()}")
    
    try:
        analyzer = SeparationEfficiencyAnalyzer()
        logger.debug("SeparationEfficiencyAnalyzer initialized")

        # Calculate basic efficiency
        logger.debug("Calculating basic efficiency metrics...")
        efficiency_results = analyzer.calculate_efficiency(
            feed_composition=input_data.feed_composition,
            product_composition=input_data.product_composition,
            mass_flow=input_data.mass_flow,
        )
        logger.debug(f"Basic efficiency results: {efficiency_results}")

        # Process component recoveries
        if "component_recoveries" in efficiency_results:
            component_order = list(input_data.feed_composition.keys())
            logger.debug(f"Processing component recoveries with order: {component_order}")
            efficiency_results["component_recoveries"] = {
                k: float(efficiency_results["component_recoveries"][k])
                for k in component_order
                if k in efficiency_results["component_recoveries"]
            }
            logger.debug(f"Processed component recoveries: {efficiency_results['component_recoveries']}")

        # Analyze process performance if data provided
        if input_data.process_data and input_data.target_purity:
            logger.debug("Analyzing process performance with additional data...")
            try:
                # Create parent data dictionary for references
                parent_data = {
                    "feed_composition": input_data.feed_composition,
                    "product_composition": input_data.product_composition,
                    "mass_flow": input_data.mass_flow
                }
                
                performance_results = analyzer.analyze_process_performance(
                    process_data=input_data.process_data,
                    target_purity=input_data.target_purity,
                    parent_data=parent_data
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
            except Exception as e:
                logger.error(f"Error in process performance analysis: {str(e)}", exc_info=True)
                raise

        # Add cleanup task
        background_tasks.add_task(logger.info, f"Completed separation analysis")
        
        logger.info("Successfully completed separation efficiency analysis")
        logger.debug(f"Final separation results: {efficiency_results}")
        return efficiency_results

    except ValueError as ve:
        logger.error(f"Validation error in separation efficiency analysis: {str(ve)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in separation efficiency analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/particle-size/", response_model=Dict[str, Union[float, Dict]])
async def analyze_particle_size(
    input_data: ParticleSizeInput,
    background_tasks: BackgroundTasks
):
    """Analyze particle size distribution"""
    logger.info("Processing particle size analysis")
    logger.debug(f"Particle size input data: {input_data.dict()}")
    
    try:
        # Generate cache key
        cache_key = _generate_cache_key(input_data)
        logger.debug(f"Generated cache key: {cache_key}")

        # Prepare particle data in the expected format
        particle_data = {
            "sizes": input_data.particle_sizes,
            "weights": input_data.weights,
            "density": input_data.density,
            "initial_moisture": input_data.initial_moisture,
            "final_moisture": input_data.final_moisture,
            "percentiles": {
                "d10": input_data.particle_sizes[0],  # First size is D10
                "d50": input_data.particle_sizes[1],  # Second size is D50
                "d90": input_data.particle_sizes[2]   # Third size is D90
            }
        }
        
        # Try to get cached results
        try:
            logger.debug("Attempting to retrieve cached results...")
            distribution_results = _cached_particle_analysis(
                cache_key=cache_key,
                particle_data=particle_data,
                treatment_type=input_data.treatment_type
            )
            logger.debug("Successfully retrieved results from cache")
        except Exception as cache_error:
            logger.warning(f"Cache retrieval failed: {str(cache_error)}")
            logger.debug("Falling back to direct calculation")
            distribution_results = particle_analyzer.process_sample(
                particle_data=particle_data,
                treatment_type=input_data.treatment_type
            )

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
                logger.error(f"Quality evaluation failed: {str(quality_error)}", exc_info=True)
                raise ValueError(f"Quality evaluation failed: {str(quality_error)}")

        # Add cleanup task
        background_tasks.add_task(logger.info, f"Completed particle size analysis for key: {cache_key}")

        logger.info("Successfully completed particle size analysis")
        logger.debug(f"Final particle size results: {distribution_results}")
        return distribution_results

    except ValueError as ve:
        logger.error(f"Validation error in particle size analysis: {str(ve)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in particle size analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/complete-analysis/", response_model=ProteinAnalysisResponse)
async def perform_complete_analysis(
    recovery_input: ProteinRecoveryInput,
    separation_input: SeparationEfficiencyInput,
    particle_input: ParticleSizeInput,
    background_tasks: BackgroundTasks
):
    """Perform comprehensive protein analysis"""
    logger.info("Starting complete protein analysis")
    logger.debug(f"Recovery input: {recovery_input.dict()}")
    logger.debug(f"Separation input: {separation_input.dict()}")
    logger.debug(f"Particle input: {particle_input.dict()}")
    
    try:
        # Get recovery metrics
        logger.debug("Processing recovery analysis...")
        recovery_metrics = await calculate_protein_recovery(recovery_input)
        logger.debug(f"Recovery metrics: {recovery_metrics}")

        # Get separation metrics
        logger.debug("Processing separation analysis...")
        separation_metrics = await analyze_separation_efficiency(separation_input, background_tasks)
        logger.debug(f"Separation metrics: {separation_metrics}")

        # Get particle metrics
        logger.debug("Processing particle size analysis...")
        particle_metrics = await analyze_particle_size(particle_input, background_tasks)
        logger.debug(f"Particle metrics: {particle_metrics}")

        # Flatten nested dictionaries in particle_metrics
        flattened_particle_metrics = {}
        for key, value in particle_metrics.items():
            if key == 'moisture_status':
                # Extract the moisture values only
                flattened_particle_metrics['pre_treatment_moisture'] = value['pre_treatment']['moisture']
                flattened_particle_metrics['post_treatment_moisture'] = value['post_treatment']['moisture']
                flattened_particle_metrics['processing_moisture'] = value['processing']['moisture']
            elif key == 'percentiles':
                # Extract percentile values
                flattened_particle_metrics['d10'] = value['d10']
                flattened_particle_metrics['d50'] = value['d50']
                flattened_particle_metrics['d90'] = value['d90']
            else:
                # Keep non-nested values as is
                if isinstance(value, (int, float)):
                    flattened_particle_metrics[key] = float(value)

        # Extract process performance metrics if available
        process_performance = None
        if "cumulative_efficiency" in separation_metrics:
            logger.debug("Extracting process performance metrics...")
            process_performance = calculate_process_performance(recovery_metrics, separation_metrics)
            logger.debug(f"Process performance metrics: {process_performance}")

        response = ProteinAnalysisResponse(
            recovery_metrics=recovery_metrics,
            separation_metrics=separation_metrics,
            particle_metrics=flattened_particle_metrics,
            process_performance=process_performance,
        )
        logger.info("Successfully completed comprehensive protein analysis")
        logger.debug(f"Final response: {response.dict()}")
        return response

    except HTTPException:
        logger.error("HTTP exception occurred during complete analysis", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in complete analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Complete analysis failed: {str(e)}")

def calculate_process_performance(recovery_data: dict, separation_data: dict) -> dict:
    # Calculate cumulative efficiency with process-type weighting
    process_type = recovery_data.get('process_type', 'rf')
    weights = {
        'rf': {'recovery': 0.4, 'separation': 0.6},
        'ir': {'recovery': 0.35, 'separation': 0.65}
    }.get(process_type, {'recovery': 0.5, 'separation': 0.5})

    cumulative_efficiency = (
        recovery_data['recovery_rate'] * weights['recovery'] +
        separation_data['separation_efficiency'] * weights['separation']
    )

    # Calculate average step efficiency with moisture adjustment
    avg_step_efficiency = (
        recovery_data['recovery_rate'] * 0.7 + 
        separation_data['separation_efficiency'] * 0.3
    ) / (0.7 + 0.3 - (max(0, 10.2 - 12) * 0.1))  # Moisture impact factor

    return {
        'cumulative_efficiency': min(cumulative_efficiency, 100),
        'average_step_efficiency': min(avg_step_efficiency, 100),
        'purity_achievement': separation_data.get('purity_achievement', 100)
    }
