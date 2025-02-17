import pytest
from fastapi.testclient import TestClient
from backend.fastapi_app.main import app
from backend.fastapi_app.models.economic_analysis import (
    ProcessType, EconomicFactors, Utility, RawMaterial, LaborConfig
)

client = TestClient(app)

def test_calculate_opex_basic():
    """Test basic OPEX calculation with minimal input"""
    # Setup utilities
    utility = Utility(
        name="Electricity",
        consumption=1000.0,
        unit_price=0.12,
        unit="kWh"
    )
    
    # Setup raw materials
    raw_material = RawMaterial(
        name="Pea Protein",
        quantity=500.0,
        unit_price=2.5,
        unit="kg"
    )
    
    # Setup labor configuration
    labor_config = LaborConfig(
        hourly_wage=25.0,
        hours_per_week=40.0,
        weeks_per_year=50.0,
        num_workers=2
    )
    
    # Setup economic factors
    economic_factors = EconomicFactors(
        installation_factor=0.2,  # Not used in OPEX
        indirect_costs_factor=0.15,  # Not used in OPEX
        maintenance_factor=0.05,
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )
    
    # Calculate expected costs
    expected_utility_cost = utility.consumption * utility.unit_price
    expected_raw_material_cost = raw_material.quantity * raw_material.unit_price
    expected_labor_cost = (
        labor_config.hourly_wage * 
        labor_config.hours_per_week * 
        labor_config.weeks_per_year * 
        labor_config.num_workers
    )
    equipment_costs = 50000.0
    expected_maintenance_cost = equipment_costs * economic_factors.maintenance_factor
    
    input_data = {
        "utilities": [utility.model_dump()],
        "raw_materials": [raw_material.model_dump()],
        "labor_config": labor_config.model_dump(),
        "equipment_costs": equipment_costs,
        "economic_factors": economic_factors.model_dump(),
        "process_type": ProcessType.BASELINE
    }
    
    response = client.post("/api/v1/economic/opex/calculate", json=input_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "opex_summary" in data
    assert "breakdowns" in data
    
    summary = data["opex_summary"]
    assert all(k in summary for k in [
        "total_opex",
        "raw_material_costs",
        "utility_costs",
        "labor_costs",
        "maintenance_costs"
    ])
    
    # Verify individual cost components
    assert summary["utility_costs"] == expected_utility_cost
    assert summary["raw_material_costs"] == expected_raw_material_cost
    assert summary["labor_costs"] == expected_labor_cost
    assert summary["maintenance_costs"] == expected_maintenance_cost
    
    # Verify total OPEX
    expected_total = (
        expected_utility_cost +
        expected_raw_material_cost +
        expected_labor_cost +
        expected_maintenance_cost
    )
    assert summary["total_opex"] == expected_total

def test_calculate_opex_empty_utilities():
    """Test OPEX calculation with empty utilities list"""
    labor_config = LaborConfig(
        hourly_wage=25.0,
        hours_per_week=40.0,
        weeks_per_year=50.0,
        num_workers=2
    )
    
    economic_factors = EconomicFactors(
        installation_factor=0.2,
        indirect_costs_factor=0.15,
        maintenance_factor=0.05,
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )
    
    input_data = {
        "utilities": [],
        "raw_materials": [],
        "labor_config": labor_config.model_dump(),
        "equipment_costs": 50000.0,
        "economic_factors": economic_factors.model_dump(),
        "process_type": ProcessType.BASELINE
    }
    
    response = client.post("/api/v1/economic/opex/calculate", json=input_data)
    assert response.status_code == 422
    assert "Missing required data" in response.json()["detail"]["error"]

def test_calculate_opex_invalid_values():
    """Test OPEX calculation with invalid values"""
    # Try with negative values
    with pytest.raises(ValueError, match="greater than 0"):
        utility = Utility(
            name="Electricity",
            consumption=-1000.0,  # Negative consumption
            unit_price=0.12,
            unit="kWh"
        )
    
    # Test with invalid labor config (negative wage)
    with pytest.raises(ValueError, match="greater than 0"):
        labor_config = LaborConfig(
            hourly_wage=-25.0,  # Negative wage
            hours_per_week=40.0,
            weeks_per_year=50.0,
            num_workers=2
        )

    # Test with valid utility but invalid raw material
    utility = Utility(
        name="Electricity",
        consumption=1000.0,
        unit_price=0.12,
        unit="kWh"
    )
    
    with pytest.raises(ValueError, match="greater than 0"):
        raw_material = RawMaterial(
            name="Pea Protein",
            quantity=-500.0,  # Negative quantity
            unit_price=2.5,
            unit="kg"
        )

def test_get_default_factors():
    """Test getting default economic factors"""
    response = client.get("/api/v1/economic/opex/factors")
    assert response.status_code == 200
    
    data = response.json()
    assert all(k in data for k in [
        "installation_factor",
        "indirect_costs_factor",
        "maintenance_factor",
        "project_duration",
        "discount_rate",
        "production_volume"
    ])
    
    # Verify OPEX-specific defaults
    assert data["maintenance_factor"] == 0.05  # Specific to OPEX
    assert data["project_duration"] == 10
    assert data["production_volume"] == 1000.0 