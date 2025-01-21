from fastapi import APIRouter, HTTPException, Response
from typing import Dict, Optional, List
from pydantic import BaseModel, Field, field_validator
import logging
import math
import json

from analytics.environmental.services.allocation_engine import AllocationEngine
from backend.fastapi_app.models.environmental_analysis import (
    AllocationRequest
)
from .services.rust_handler import RustHandler

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["environmental-allocation"])

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            if math.isnan(obj):
                return 0.0
            if math.isinf(obj):
                return float('inf') if obj > 0 else float('-inf')
        return super().default(obj)

class AllocationRequest(BaseModel):
    impacts: Dict[str, float]
    product_values: Dict[str, float]
    mass_flows: Dict[str, float]
    method: str = Field(default="hybrid", pattern="^(economic|physical|hybrid)$")
    hybrid_weights: Optional[Dict[str, float]] = None

    @field_validator('impacts', 'product_values', 'mass_flows')
    @classmethod
    def validate_positive_values(cls, v: Dict[str, float]) -> Dict[str, float]:
        for key, value in v.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"Value for {key} must be a number")
            if math.isnan(value) or math.isinf(value):
                raise ValueError(f"Value for {key} cannot be NaN or infinite")
            if value < 0:
                raise ValueError(f"Value for {key} must be positive")
        return v

    @field_validator('hybrid_weights')
    @classmethod
    def validate_hybrid_weights(cls, v: Optional[Dict[str, float]]) -> Optional[Dict[str, float]]:
        if v is not None:
            if 'economic' not in v or 'physical' not in v:
                raise ValueError("Hybrid weights must contain 'economic' and 'physical' keys")
            if not math.isclose(v['economic'] + v['physical'], 1.0, rel_tol=1e-9):
                raise ValueError("Hybrid weights must sum to 1.0")
            for key, value in v.items():
                if not 0 <= value <= 1:
                    raise ValueError(f"Weight for {key} must be between 0 and 1")
        return v

# Initialize services
allocation_engine = AllocationEngine()
rust_handler = RustHandler()
logger.info("Initialized Allocation services")

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

@router.post("/calculate")
async def allocate_impacts(request: AllocationRequest):
    """Allocate environmental impacts between products"""
    try:
        logger.debug(f"Received allocation request: {request.dict()}")
        logger.info(f"Starting impact allocation using {request.method} method")

        # Validate that product_values and mass_flows have the same keys
        products = set(request.product_values.keys())
        if set(request.mass_flows.keys()) != products:
            raise ValueError("Product values and mass flows must have the same product keys")

        try:
            # Configure allocation engine with process data
            allocation_engine.configure_allocation(
                product_values=request.product_values,
                mass_flows=request.mass_flows,
                hybrid_weights=request.hybrid_weights
            )

            # Convert dictionary values to lists, ensuring matching order
            products_list = list(products)
            impact_values = []
            for impact_type in request.impacts.values():
                # Replicate impact value for each product to match length
                impact_values.extend([impact_type] * len(products_list))

            # Use Rust for performance-critical calculations
            if request.method == "economic":
                # Get economic allocation factors using Rust
                economic_values = [request.product_values[product] for product in products_list]
                economic_values = economic_values * len(request.impacts)  # Replicate for each impact type
                rust_results = rust_handler.calculate_allocation_factors(
                    impact_values,
                    economic_values
                )
                allocation_factors = rust_results["allocation_factors"]
            elif request.method == "physical":
                # Get physical allocation factors using Rust
                mass_values = [request.mass_flows[product] for product in products_list]
                mass_values = mass_values * len(request.impacts)  # Replicate for each impact type
                rust_results = rust_handler.calculate_allocation_factors(
                    impact_values,
                    mass_values
                )
                allocation_factors = rust_results["allocation_factors"]
            else:  # hybrid
                # Calculate hybrid allocation using both services
                weights = request.hybrid_weights or {"physical": 0.5, "economic": 0.5}
                
                # Get base factors using Rust with matched lengths
                economic_values = [request.product_values[product] for product in products_list]
                economic_values = economic_values * len(request.impacts)
                mass_values = [request.mass_flows[product] for product in products_list]
                mass_values = mass_values * len(request.impacts)
                
                economic_results = rust_handler.calculate_allocation_factors(
                    impact_values,
                    economic_values
                )
                physical_results = rust_handler.calculate_allocation_factors(
                    impact_values,
                    mass_values
                )
                
                # Calculate final hybrid factors
                allocation_factors = rust_handler.calculate_hybrid_allocation_factors(
                    physical_results["allocation_factors"],
                    economic_results["allocation_factors"],
                    weights["physical"]
                )

            # Use allocation engine to get final allocated impacts
            allocated_impacts = allocation_engine.allocate_impacts(
                request.impacts,
                method=request.method
            )

            # Map results back to product keys
            allocated_results = {
                "allocation_factors": dict(zip(products_list, allocation_factors[:len(products_list)])),
                "allocated_impacts": allocated_impacts
            }

            logger.info("Impact allocation completed successfully")
            
            # Get allocation factors based on method
            method_factors = allocation_engine.get_allocation_factors(
                'hybrid' if request.method == 'hybrid' else request.method
            )
            
            return create_json_response({
                "status": "success",
                "method": request.method,
                "results": allocated_results,
                "allocation_factors": method_factors
            })

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        except RuntimeError as e:
            logger.error(f"Calculation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error in impact allocation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/methods")
async def get_allocation_methods():
    """Get available allocation methods and their descriptions"""
    try:
        logger.debug("Retrieving allocation methods")
        return create_json_response({
            "economic": "Allocation based on economic value of products ($/kg)",
            "physical": "Allocation based on mass flows of products (kg)",
            "hybrid": "Combined economic and physical allocation with configurable weights"
        })
    except Exception as e:
        error_msg = f"Error retrieving allocation methods: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg) 