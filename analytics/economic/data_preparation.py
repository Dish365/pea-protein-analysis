from typing import Dict, Any, List

def prepare_equipment_data(equipment_cost: float, maintenance_cost: float, 
                         electricity_consumption: float, production_volume: float) -> Dict[str, Any]:
    """Prepare standardized equipment data"""
    return {
        "name": "main_equipment",
        "cost": equipment_cost,
        "efficiency": 1.0,
        "maintenance_cost": maintenance_cost,
        "energy_consumption": electricity_consumption,
        "processing_capacity": production_volume
    }

def get_default_indirect_factors(equipment_cost: float) -> List[Dict[str, Any]]:
    """Get default indirect cost factors"""
    return [
        {
            "name": "engineering",
            "cost": equipment_cost,
            "percentage": 0.15
        },
        {
            "name": "contingency",
            "cost": equipment_cost,
            "percentage": 0.10
        },
        {
            "name": "construction",
            "cost": equipment_cost,
            "percentage": 0.20
        }
    ]

def prepare_economic_factors(project_duration: int, discount_rate: float,
                           production_volume: float, installation_factor: float = 0.2,
                           indirect_costs_factor: float = 0.15,
                           maintenance_factor: float = 0.05) -> Dict[str, Any]:
    """Prepare standardized economic factors"""
    return {
        "installation_factor": installation_factor,
        "indirect_costs_factor": indirect_costs_factor,
        "maintenance_factor": maintenance_factor,
        "project_duration": project_duration,
        "discount_rate": discount_rate,
        "production_volume": production_volume
    } 