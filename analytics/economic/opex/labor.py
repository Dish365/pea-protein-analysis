# Implement labor cost management

def calculate_labor_costs(hourly_wage, hours_per_week, weeks_per_year, num_workers):
    """
    Calculate labor costs based on hourly wage, hours per week, weeks per year, and number of workers.
    """
    annual_hours = hours_per_week * weeks_per_year
    total_labor_costs = hourly_wage * annual_hours * num_workers
    return total_labor_costs