import pytest
from fastapi.testclient import TestClient
from backend.fastapi_app.main import app
from backend.fastapi_app.models.economic_analysis import ProcessType, Equipment, EconomicFactors, IndirectFactor

client = TestClient(app)

def test_calculate_capex_basic():
    """Test basic CAPEX calculation with minimal input"""
    base_cost = 50000.0
    efficiency_factor = 0.85
    installation_complexity = 1.2
    expected_equipment_cost = base_cost * (1 + efficiency_factor) * installation_complexity
    
    equipment = Equipment(
        name="Centrifuge",
        base_cost=base_cost,
        efficiency_factor=efficiency_factor,
        installation_complexity=installation_complexity,
        maintenance_cost=2500.0,
        energy_consumption=15.0,
        processing_capacity=1000.0
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
        "equipment_list": [equipment.model_dump()],
        "economic_factors": economic_factors.model_dump(),
        "process_type": ProcessType.BASELINE
    }
    
    response = client.post("/api/v1/economic/capex/calculate", json=input_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "capex_summary" in data
    assert "equipment_breakdown" in data
    assert "indirect_factors" in data
    
    summary = data["capex_summary"]
    assert all(k in summary for k in ["total_capex", "equipment_costs", "installation_costs", "indirect_costs"])
    assert summary["equipment_costs"] == expected_equipment_cost
    assert summary["total_capex"] > summary["equipment_costs"]

def test_calculate_capex_with_indirect_factors():
    """Test CAPEX calculation with custom indirect factors"""
    base_cost = 50000.0
    efficiency_factor = 0.85
    installation_complexity = 1.2
    expected_equipment_cost = base_cost * (1 + efficiency_factor) * installation_complexity
    
    equipment = Equipment(
        name="Centrifuge",
        base_cost=base_cost,
        efficiency_factor=efficiency_factor,
        installation_complexity=installation_complexity,
        maintenance_cost=2500.0,
        energy_consumption=15.0,
        processing_capacity=1000.0
    )
    
    indirect_factor = IndirectFactor(
        name="Engineering",
        cost=10000.0,
        percentage=0.15
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
        "equipment_list": [equipment.model_dump()],
        "indirect_factors": [indirect_factor.model_dump()],
        "economic_factors": economic_factors.model_dump(),
        "process_type": ProcessType.BASELINE
    }
    
    response = client.post("/api/v1/economic/capex/calculate", json=input_data)
    assert response.status_code == 200
    
    data = response.json()
    factors = data["indirect_factors"]
    assert factors["source"] == "user"
    assert len(factors["factors"]) == 1
    assert factors["factors"][0]["name"] == "Engineering"
    
    summary = data["capex_summary"]
    assert summary["equipment_costs"] == expected_equipment_cost

def test_calculate_capex_empty_equipment():
    """Test CAPEX calculation with empty equipment list"""
    economic_factors = EconomicFactors(
        installation_factor=0.2,
        indirect_costs_factor=0.15,
        maintenance_factor=0.05,
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )
    
    input_data = {
        "equipment_list": [],
        "economic_factors": economic_factors.model_dump(),
        "process_type": ProcessType.BASELINE
    }
    
    response = client.post("/api/v1/economic/capex/calculate", json=input_data)
    assert response.status_code == 422

def test_get_default_factors():
    """Test getting default economic factors"""
    response = client.get("/api/v1/economic/capex/factors")
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