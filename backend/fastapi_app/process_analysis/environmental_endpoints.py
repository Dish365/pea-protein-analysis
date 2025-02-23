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
    Analyze environmental impacts of a process and optionally perform allocation
    
    This endpoint combines impact calculation and allocation in a single call:
    1. Calculates environmental impacts (GWP, HCT, FRS, Water)
    2. Optionally performs impact allocation if allocation data is provided
    3. Returns detailed results including process contributions
    """
    # Log request details
    await log_request_details(request)
    logger.info("Starting process analysis")
    
    try:
        # Log input validation
        logger.debug("Validating process inputs")
        logger.debug(f"Process Inputs: {analysis_request.request.dict()}")
        if analysis_request.allocation_method:
            logger.debug(f"Allocation Method: {analysis_request.allocation_method}")
            logger.debug(f"Product Values: {analysis_request.product_values}")
            logger.debug(f"Mass Flows: {analysis_request.mass_flows}")
            logger.debug(f"Hybrid Weights: {analysis_request.hybrid_weights}")

        # Calculate impacts
        logger.info("Calculating environmental impacts")
        impact_results = impact_calculator.calculate_process_impacts(**analysis_request.request.dict())
        logger.debug(f"Impact Results: {impact_results}")
        
        detailed_results = impact_calculator.get_detailed_results()
        if not detailed_results:
            logger.error("Failed to get detailed impact results")
            raise RuntimeError("Failed to get detailed impact results")
        
        logger.debug(f"Detailed Results: {detailed_results}")
        
        # Determine if allocation should be performed
        allocation_results = None
        if analysis_request.allocation_method:
            logger.info(f"Performing {analysis_request.allocation_method} allocation")
            
            # Validate allocation data
            try:
                if analysis_request.allocation_method == AllocationMethod.ECONOMIC and not analysis_request.product_values:
                    raise ValueError("Product values required for economic allocation")
                if analysis_request.allocation_method == AllocationMethod.PHYSICAL and not analysis_request.mass_flows:
                    raise ValueError("Mass flows required for physical allocation")
                if analysis_request.allocation_method == AllocationMethod.HYBRID:
                    if not analysis_request.product_values or not analysis_request.mass_flows:
                        raise ValueError("Product values and mass flows required for hybrid allocation")
                    if not analysis_request.hybrid_weights:
                        logger.info("Using default hybrid weights (0.5, 0.5)")
                        analysis_request.hybrid_weights = AllocationWeights(economic=0.5, physical=0.5)
            
                allocation_data = AllocationRequest(
                    impacts=impact_results,
                    product_values=analysis_request.product_values or {},
                    mass_flows=analysis_request.mass_flows or {},
                    method=analysis_request.allocation_method,
                    hybrid_weights=analysis_request.hybrid_weights
                )
                
                logger.debug(f"Allocation Request: {allocation_data.dict()}")
                allocation_response = await allocate_impacts(allocation_data)
                # Parse the FastAPI Response object to get the JSON data
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
        
        # Determine suggested allocation method
        suggested_method = (
            analysis_request.allocation_method or
            AllocationMethod.PHYSICAL if detailed_results["metadata"]["thermal_ratio"] > 0.7
            else AllocationMethod.ECONOMIC if detailed_results["metadata"]["total_mass"] < 100
            else AllocationMethod.HYBRID
        )
        logger.debug(f"Suggested Allocation Method: {suggested_method}")
        
        # Prepare response
        if not include_contributions:
            detailed_results["process_contributions"] = {}
            logger.debug("Process contributions excluded from response")
            
        response_data = ProcessAnalysisResponse(
            status="success",
            impact_results=detailed_results,
            allocation_results=allocation_results,
            suggested_allocation_method=suggested_method
        )
        
        logger.info("Process analysis completed successfully")
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