from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel

from analytics.environmental.services.allocation_engine import AllocationEngine

router = APIRouter(prefix="/allocation", tags=["environmental-allocation"])

class AllocationRequest(BaseModel):
    impacts: Dict[str, float]
    product_values: Dict[str, float]
    mass_flows: Dict[str, float]
    method: str = "hybrid"
    hybrid_weights: Optional[Dict[str, float]] = None

# Initialize allocation engine
allocation_engine = AllocationEngine()

@router.post("/calculate")
async def allocate_impacts(request: AllocationRequest):
    """Allocate environmental impacts between products"""
    try:
        allocation_engine.configure_allocation(
            product_values=request.product_values,
            mass_flows=request.mass_flows,
            hybrid_weights=request.hybrid_weights
        )
        
        allocated_impacts = allocation_engine.allocate_impacts(
            impacts=request.impacts,
            method=request.method
        )
        
        return {
            "status": "success",
            "allocated_impacts": allocated_impacts,
            "allocation_factors": allocation_engine.get_allocation_factors(request.method)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/methods")
async def get_allocation_methods():
    """Get available allocation methods and their descriptions"""
    return {
        "economic": "Allocation based on economic value",
        "physical": "Allocation based on mass flows",
        "hybrid": "Combined economic and physical allocation"
    } 