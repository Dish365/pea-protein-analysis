from typing import Dict, List

def calculate_labor_costs(
    hourly_wage: float,
    hours_per_week: float,
    weeks_per_year: float,
    num_workers: int,
    overtime_factor: float = 1.5,
    overtime_hours: float = 0.0
) -> float:
    """
    Calculate total labor costs including regular time and overtime.
    Based on paper Section 3.2.2
    
    Args:
        hourly_wage: Base hourly wage rate
        hours_per_week: Regular working hours per week
        weeks_per_year: Working weeks per year
        num_workers: Number of workers
        overtime_factor: Overtime pay multiplier (default: 1.5)
        overtime_hours: Additional overtime hours per week (default: 0.0)
        
    Returns:
        float: Total annual labor costs
        
    Raises:
        ValueError: If any input parameters are invalid
    """
    # Validate inputs
    if hourly_wage <= 0:
        raise ValueError("Hourly wage must be positive")
        
    if hours_per_week < 0 or hours_per_week > 168:  # 168 hours in a week
        raise ValueError("Hours per week must be between 0 and 168")
        
    if weeks_per_year < 0 or weeks_per_year > 52:
        raise ValueError("Weeks per year must be between 0 and 52")
        
    if num_workers < 0:
        raise ValueError("Number of workers cannot be negative")
        
    if overtime_factor < 1:
        raise ValueError("Overtime factor must be greater than or equal to 1")
        
    if overtime_hours < 0:
        raise ValueError("Overtime hours cannot be negative")
        
    # Calculate regular time costs
    regular_hours_per_year = hours_per_week * weeks_per_year
    regular_costs = hourly_wage * regular_hours_per_year * num_workers
    
    # Calculate overtime costs
    overtime_hours_per_year = overtime_hours * weeks_per_year
    overtime_costs = (hourly_wage * overtime_factor * overtime_hours_per_year * num_workers)
    
    # Total labor costs
    total_labor_costs = regular_costs + overtime_costs
    
    return total_labor_costs