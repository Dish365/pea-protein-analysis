from fastapi import APIRouter, HTTPException, Response, Header, Query, Request, Body
from typing import Dict, Optional, Any
import logging
import json
import traceback
from datetime import datetime
from pydantic import BaseModel

from analytics.environmental.services.impact_calculator import ImpactCalculator
from backend.fastapi_app.models.environmental_analysis import (
    AllocationMethod,
    ProcessInputs,
    AllocationRequest,
    ProcessAnalysisResponse,
    AllocationWeights
)
from .allocation_endpoints import allocate_impacts

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add file handler for persistent logging
file_handler = logging.FileHandler('environmental_endpoints.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)

# Initialize services
impact_calculator = ImpactCalculator()
logger.info("Initialized ImpactCalculator service")

class EnvironmentalAnalysisRequest(BaseModel):
    """Request model for environmental analysis"""
    request: ProcessInputs
    allocation_method: Optional[AllocationMethod] = None
    product_values: Optional[Dict[str, float]] = None
    mass_flows: Optional[Dict[str, float]] = None
    hybrid_weights: Optional[AllocationWeights] = None

async def log_request_details(request: Request) -> None:
    """Log detailed request information"""
    body = await request.body()
    logger.debug("=== Request Details ===")
    logger.debug(f"Method: {request.method}")
    logger.debug(f"URL: {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    logger.debug(f"Query Params: {dict(request.query_params)}")
    try:
        if body:
            logger.debug(f"Body: {json.loads(body)}")
    except json.JSONDecodeError:
        logger.debug(f"Raw Body: {body}")

def log_validation_error(error: Exception, data: Any) -> None:
    """Log validation error details"""
    logger.error("=== Validation Error ===")
    logger.error(f"Error Type: {type(error).__name__}")
    logger.error(f"Error Message: {str(error)}")
    logger.error(f"Invalid Data: {data}")
    logger.error(f"Stack Trace: {traceback.format_exc()}")

router = APIRouter(tags=["environmental-impact"])

@router.post("/analyze-process", response_model=ProcessAnalysisResponse)
async def analyze_process(
    request: Request,
    analysis_request: EnvironmentalAnalysisRequest,
    include_contributions: bool = Query(True, description="Include process contributions in response")
) -> ProcessAnalysisResponse:
    """
    Analyze environmental impacts of RF-treated pea protein process
    
    This endpoint performs comprehensive analysis including:
    1. RF treatment parameter validation
    2. Process step impact calculations
    3. Environmental impact assessment
    4. Optional impact allocation
    5. Process validation against research benchmarks
    """
    # Log request details
    await log_request_details(request)
    logger.info("Starting RF process analysis")
    
    try:
        # Validate RF process parameters
        logger.debug("Validating RF process parameters")
        process_inputs = analysis_request.request
        
        # Comprehensive RF parameter validation
        rf_validation = {
            "temperature": {
                "outfeed": {
                    "value": process_inputs.rf_temperature_outfeed_c,
                    "within_range": 80 <= process_inputs.rf_temperature_outfeed_c <= 90,
                    "optimal": 84.4,
                    "tolerance": "±5°C"
                },
                "electrode": {
                    "value": process_inputs.rf_temperature_electrode_c,
                    "within_range": 95 <= process_inputs.rf_temperature_electrode_c <= 105,
                    "optimal": 100.1,
                    "tolerance": "±5°C"
                }
            },
            "moisture": {
                "initial": process_inputs.initial_moisture_content,
                "final": process_inputs.final_moisture_content,
                "target": process_inputs.target_moisture_content,
                "reduction": process_inputs.initial_moisture_content - process_inputs.final_moisture_content,
                "within_range": 0.03 <= (process_inputs.initial_moisture_content - process_inputs.final_moisture_content) <= 0.04,
                "optimal_reduction": 0.034,
                "tolerance": "±0.005"
            }
        }
        
        # Log validation warnings
        if not rf_validation["temperature"]["outfeed"]["within_range"]:
            logger.warning(f"Outfeed temperature {process_inputs.rf_temperature_outfeed_c}°C outside optimal range (80-90°C)")
        if not rf_validation["temperature"]["electrode"]["within_range"]:
            logger.warning(f"Electrode temperature {process_inputs.rf_temperature_electrode_c}°C outside optimal range (95-105°C)")
        if not rf_validation["moisture"]["within_range"]:
            logger.warning(f"Moisture reduction {rf_validation['moisture']['reduction']:.3f} outside expected range (0.03-0.04)")
            
        # Calculate total energy consumption
        total_energy = (
            process_inputs.rf_electricity_kwh +
            process_inputs.air_classifier_milling_kwh +
            process_inputs.air_classification_kwh +
            process_inputs.hammer_milling_kwh +
            process_inputs.dehulling_kwh
        )
        
        # Calculate RF energy contribution
        rf_contribution = process_inputs.rf_electricity_kwh / total_energy if total_energy > 0 else 0
        if not (0.18 <= rf_contribution <= 0.20):  # 19% ± 1% from research
            logger.warning(f"RF energy contribution {rf_contribution:.3f} outside expected range (0.18-0.20)")
        
        # Calculate impacts
        logger.info("Calculating environmental impacts")
        impact_results = impact_calculator.calculate_process_impacts(**process_inputs.dict())
        logger.debug(f"Impact Results: {impact_results}")
        
        detailed_results = impact_calculator.get_detailed_results()
        if not detailed_results:
            logger.error("Failed to get detailed impact results")
            raise RuntimeError("Failed to get detailed impact results")
        
        # Add process breakdown
        detailed_results['process_breakdown'] = {
            'air_classifier_milling': 0.21,  # ~21% contribution
            'air_classification': 0.21,      # ~21% contribution
            'rf_treatment': 0.19,            # ~19% contribution
            'tempering': 0.144,              # ~14.4% contribution
            'hammer_milling': 0.13,          # ~13% contribution
            'dehulling': 0.16                # ~16% contribution
        }
        
        # Perform allocation if requested
        allocation_results = None
        if analysis_request.allocation_method:
            logger.info(f"Performing {analysis_request.allocation_method} allocation")
            
            try:
                # Validate allocation data
                if analysis_request.allocation_method == AllocationMethod.ECONOMIC and not analysis_request.product_values:
                    raise ValueError("Product values required for economic allocation")
                if analysis_request.allocation_method == AllocationMethod.PHYSICAL and not analysis_request.mass_flows:
                    raise ValueError("Mass flows required for physical allocation")
                if analysis_request.allocation_method == AllocationMethod.HYBRID:
                    if not analysis_request.product_values or not analysis_request.mass_flows:
                        raise ValueError("Product values and mass flows required for hybrid allocation")
                    if not analysis_request.hybrid_weights:
                        logger.info("Using research-based hybrid weights (0.6, 0.4)")
                        analysis_request.hybrid_weights = AllocationWeights(economic=0.6, physical=0.4)
            
                allocation_data = AllocationRequest(
                    impacts=impact_results,
                    product_values=analysis_request.product_values or {},
                    mass_flows=analysis_request.mass_flows or {},
                    method=analysis_request.allocation_method,
                    hybrid_weights=analysis_request.hybrid_weights
                )
                
                logger.debug(f"Allocation Request: {allocation_data.dict()}")
                allocation_response = await allocate_impacts(allocation_data)
                response_data = json.loads(allocation_response.body)
                allocation_results = response_data.get("results")
                logger.debug(f"Allocation Results: {allocation_results}")
                
            except ValueError as e:
                log_validation_error(e, {
                    "allocation_method": analysis_request.allocation_method,
                    "product_values": analysis_request.product_values,
                    "mass_flows": analysis_request.mass_flows,
                    "hybrid_weights": analysis_request.hybrid_weights
                })
                raise HTTPException(status_code=422, detail={"message": str(e), "type": "allocation_error"})
        
        # Determine suggested allocation method based on research
        suggested_method = AllocationMethod.ECONOMIC  # Default based on research
        
        # Update RF validation metrics in response
        rf_validation.update({
            "energy_efficiency": {
                "value": rf_contribution,
                "within_range": 0.18 <= rf_contribution <= 0.20,
                "optimal": 0.19,
                "tolerance": "±0.01"
            },
            "process_contribution": detailed_results['process_breakdown']['rf_treatment']
        })
        
        # Prepare response
        if not include_contributions:
            detailed_results["process_contributions"] = {}
            logger.debug("Process contributions excluded from response")
            
        response_data = ProcessAnalysisResponse(
            status="success",
            impact_results=detailed_results,
            allocation_results=allocation_results,
            suggested_allocation_method=suggested_method,
            rf_validation=rf_validation
        )
        
        logger.info("RF process analysis completed successfully")
        logger.debug(f"Response Data: {response_data.dict()}")
        return response_data
        
    except ValueError as e:
        log_validation_error(e, analysis_request.dict())
        raise HTTPException(status_code=422, detail={"message": str(e), "type": "validation_error"})
    except RuntimeError as e:
        logger.error(f"Calculation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"message": str(e), "type": "calculation_error"})
    except Exception as e:
        logger.error(f"Unexpected error in process analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"message": str(e), "type": "server_error"})

@router.get("/impact-factors")
async def get_impact_factors(request: Request):
    """Get environmental impact factors used in calculations"""
    await log_request_details(request)
    
    try:
        logger.info("Retrieving impact factors")
        impact_factors = impact_calculator.get_impact_factors()
        logger.debug(f"Impact Factors: {impact_factors}")
        return impact_factors
    except Exception as e:
        logger.error(f"Error retrieving impact factors: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"message": str(e), "type": "server_error"}
        ) 