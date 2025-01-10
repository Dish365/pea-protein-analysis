# Implement OPEX-related API endpoints

from fastapi import APIRouter

router = APIRouter()

@router.get("/opex")
def get_opex_data():
    # Placeholder for OPEX data retrieval logic
    opex_data = {
        "labor_costs": 50000,
        "maintenance_costs": 20000,
        "utility_costs": 15000,
        "raw_material_costs": 30000,
        "total_opex": 115000
    }
    return opex_data
