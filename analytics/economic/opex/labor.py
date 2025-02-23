from typing import Dict, Any
from math import ceil


def calculate_labor_costs(labor_config: Dict[str, Any], production_volume: float) -> Dict[str, Any]:
    """
    Calculate labor costs with proper scaling based on production volume.
    Accounts for multiple shifts and worker requirements based on scale.
    
    Args:
        labor_config: Dictionary containing:
            - hourly_wage: Base hourly wage per worker
            - hours_per_week: Standard hours per week per shift
            - weeks_per_year: Working weeks per year
            - benefits_factor: Additional benefits as fraction of base wage
        production_volume: Annual production volume in kg
            
    Returns:
        Dictionary containing:
        - total_cost: Total annual labor cost
        - direct_labor: Direct labor cost
        - benefits: Cost of benefits
        - shifts: Number of shifts required
        - workers_per_shift: Number of workers per shift
        - total_workers: Total number of workers
        
    Raises:
        ValueError: If labor configuration is invalid
    """
    # Validate inputs
    required_fields = ["hourly_wage", "hours_per_week", "weeks_per_year", "benefits_factor"]
    if not all(field in labor_config for field in required_fields):
        raise ValueError(f"Labor config must contain all required fields: {required_fields}")
        
    if production_volume <= 0:
        raise ValueError("Production volume must be positive")
        
    # Constants for labor scaling
    BASE_VOLUME = 1000000  # 1000 metric tons per year
    BASE_WORKERS_PER_SHIFT = 4  # Base number of workers for BASE_VOLUME
    MAX_VOLUME_PER_WORKER = 500000  # Maximum kg per worker per year
    
    # Calculate required number of workers based on production volume
    workers_per_shift = ceil(
        BASE_WORKERS_PER_SHIFT * 
        (production_volume / BASE_VOLUME) ** 0.7  # Use 0.7 power rule for labor scaling
    )
    
    # Calculate required shifts based on production volume
    annual_hours_per_shift = labor_config["hours_per_week"] * labor_config["weeks_per_year"]
    volume_per_worker_hour = MAX_VOLUME_PER_WORKER / annual_hours_per_shift
    
    required_worker_hours = production_volume / volume_per_worker_hour
    total_available_hours = workers_per_shift * annual_hours_per_shift
    
    num_shifts = ceil(required_worker_hours / total_available_hours)
    num_shifts = min(max(num_shifts, 1), 3)  # Limit to 1-3 shifts
    
    # Calculate total number of workers
    total_workers = workers_per_shift * num_shifts
    
    # Calculate annual base labor cost
    annual_hours = (
        labor_config["hours_per_week"] * 
        labor_config["weeks_per_year"]
    )
    
    base_labor_cost = (
        labor_config["hourly_wage"] * 
        annual_hours * 
        total_workers
    )
    
    # Calculate benefits
    benefits_cost = base_labor_cost * labor_config["benefits_factor"]
    
    # Calculate total cost
    total_cost = base_labor_cost + benefits_cost
    
    return {
        "total_cost": total_cost,
        "direct_labor": base_labor_cost,
        "benefits": benefits_cost,
        "shifts": num_shifts,
        "workers_per_shift": workers_per_shift,
        "total_workers": total_workers
    }
