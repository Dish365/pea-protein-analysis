from fastapi import APIRouter, HTTPException, Response, Header
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator
import logging
import math
import json

from analytics.environmental.services.impact_calculator import ImpactCalculator
from analytics.environmental.impact.gwp import GWPCalculator
from analytics.environmental.impact.hct import HCTCalculator
from analytics.environmental.impact.frs import FRSCalculator
from analytics.environmental.impact.water import WaterConsumptionCalculator
from backend.fastapi_app.models.environmental_analysis import (
    AllocationRequest
)
from .allocation_endpoints import allocate_impacts

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["environmental-impact"])

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            if math.isnan(obj):
                logger.debug(f"Converting NaN to 0.0")
                return 0.0
            if math.isinf(obj):
                logger.debug(f"Converting infinite value to bounded value")
                if obj > 0:
                    return 1.7976931348623157e+308  # Max float value
                return -1.7976931348623157e+308
        return super().default(obj)

class ProcessData(BaseModel):
    electricity_kwh: float
    water_kg: float
    transport_ton_km: float
    product_kg: float
    equipment_kg: float
    cooling_kwh: float
    waste_kg: float
    thermal_ratio: float

    @field_validator('*')
    @classmethod
    def validate_positive_numbers(cls, v: float, field: str) -> float:
        if not isinstance(v, (int, float)):
            raise HTTPException(
                status_code=422,
                detail=f"{field.name} must be a number"
            )
        if math.isinf(v) or math.isnan(v):
            raise HTTPException(
                status_code=422,
                detail=f"{field.name} cannot be infinity or NaN"
            )
        if v < 0:
            raise HTTPException(
                status_code=422,
                detail=f"{field.name} must be positive"
            )
        if v > 1e308:
            raise HTTPException(
                status_code=422,
                detail=f"{field.name} is too large"
            )
        return v

    @field_validator('thermal_ratio')
    @classmethod
    def validate_thermal_ratio(cls, v: float) -> float:
        if not (0 <= v <= 1):
            raise HTTPException(
                status_code=422,
                detail="thermal_ratio must be between 0 and 1"
            )
        return v

class AllocationReadyResponse(BaseModel):
    """Response model that's ready for allocation processing"""
    impacts: Dict[str, float]
    process_contributions: Dict[str, Dict[str, float]]
    allocation_ready: bool = True
    suggested_allocation_method: Optional[str] = None

# Initialize calculators
impact_calculator = ImpactCalculator()
logger.info("Initialized ImpactCalculator service")

def create_json_response(content: Dict) -> Response:
    """Create a JSON response with custom encoder for handling special float values"""
    try:
        return Response(
            content=json.dumps(content, cls=CustomJSONEncoder),
            media_type="application/json"
        )
    except ValueError as e:
        logger.error(f"JSON serialization error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error serializing response data")

@router.post("/calculate-impacts")
async def calculate_impacts(data: ProcessData) -> AllocationReadyResponse:
    """
    Calculate all environmental impacts for the process
    Returns data in a format ready for allocation processing
    """
    try:
        logger.debug(f"Received impact calculation request: {data.dict()}")
        logger.info("Starting impact calculations...")

        try:
            logger.debug("Calling impact calculator with validated data")
            impacts = impact_calculator.calculate_process_impacts(**data.dict())
            logger.debug(f"Impact calculation successful: {impacts}")
            
            # Validate calculation results
            if any(math.isinf(value) or math.isnan(value) for value in impacts.values()):
                raise HTTPException(
                    status_code=422,
                    detail={"message": "Calculation resulted in invalid values (inf or NaN)", "type": "calculation_error"}
                )
                
        except ValueError as e:
            logger.error(f"Calculation error: {str(e)}")
            raise HTTPException(status_code=422, detail={"message": str(e), "type": "calculation_error"})
        except Exception as e:
            logger.error(f"Unexpected calculation error: {str(e)}")
            raise HTTPException(status_code=500, detail={"message": str(e), "type": "server_error"})

        logger.debug(f"Getting process contributions")
        process_contributions = impact_calculator.get_process_contributions()
        logger.debug(f"Process contributions: {process_contributions}")

        # Determine suggested allocation method based on process characteristics
        suggested_method = "hybrid"
        if data.thermal_ratio > 0.7:  # High thermal processing
            suggested_method = "physical"
        elif data.product_kg < 100:  # Small batch processing
            suggested_method = "economic"

        logger.info("Impact calculations completed successfully")
        
        response_data = {
            "status": "success",
            "impacts": impacts,
            "process_contributions": process_contributions,
            "allocation_ready": True,
            "suggested_allocation_method": suggested_method,
            "metadata": {
                "total_mass": data.product_kg,
                "energy_intensity": data.electricity_kwh / data.product_kg if data.product_kg > 0 else 0,
                "water_intensity": data.water_kg / data.product_kg if data.product_kg > 0 else 0
            }
        }
        
        return create_json_response(response_data)
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error in impact calculation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail={"message": error_msg, "type": "server_error"})

@router.get("/impact-factors")
async def get_impact_factors(accept: str = Header(None)):
    """Get environmental impact factors used in calculations"""
    try:
        logger.debug(f"Received impact factors request with Accept header: {accept}")
        
        # Validate Accept header
        if accept and accept != "application/json" and accept != "*/*":
            logger.warning(f"Invalid Accept header: {accept}")
            raise HTTPException(
                status_code=406,
                detail="Only application/json is supported"
            )
            
        logger.info("Retrieving environmental impact factors")
        factors = {
            "gwp_factors": GWPCalculator.GWP_FACTORS,
            "hct_factors": HCTCalculator.HCT_FACTORS,
            "frs_factors": FRSCalculator.FRS_FACTORS,
            "water_factors": WaterConsumptionCalculator.WATER_FACTORS
        }
        logger.debug(f"Retrieved impact factors: {factors}")
        
        return create_json_response(factors)
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error retrieving impact factors: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail={"message": error_msg, "type": "server_error"})

@router.post("/calculate-and-allocate")
async def calculate_impacts_and_allocate(
    data: ProcessData,
    allocation_request: Optional[Dict[str, Any]] = None
):
    """
    Calculate impacts and optionally perform allocation in one step
    """
    try:
        # First calculate impacts
        impact_response = await calculate_impacts(data)
        impact_data = json.loads(impact_response.body)
        
        # If allocation request is provided, proceed with allocation
        if allocation_request:
            logger.info("Proceeding with allocation after impact calculation")
            
            # Prepare allocation request
            allocation_data = {
                "impacts": impact_data["impacts"],
                "product_values": allocation_request.get("product_values", {}),
                "mass_flows": allocation_request.get("mass_flows", {}),
                "method": allocation_request.get("method", impact_data["suggested_allocation_method"]),
                "hybrid_weights": allocation_request.get("hybrid_weights")
            }
            
            # Forward to allocation endpoint
            allocation_response = await allocate_impacts(AllocationRequest(**allocation_data))
            
            # Combine responses
            return create_json_response({
                "status": "success",
                "impact_results": impact_data,
                "allocation_results": allocation_response["results"]
            })
            
        return impact_response
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in combined impact calculation and allocation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail={"message": error_msg, "type": "server_error"}) 