import pytest
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

@pytest.fixture
def valid_eco_efficiency_request() -> Dict[str, Any]:
    """Fixture providing valid eco-efficiency request data"""
    return {
        "economic_data": {
            "capex": 1000000.0,
            "opex": 200000.0,
            "production_volume": 5000.0,
            "product_prices": {"main_product": 100.0, "by_product": 50.0},
            "production_volumes": {"main_product": 4000.0, "by_product": 1000.0},
            "raw_material_cost": 150000.0,
            "npv": 800000.0,
            "net_profit": 300000.0
        },
        "quality_metrics": {
            "recovered_protein": 450.0,
            "initial_protein": 500.0,
            "protein_content": 0.85,
            "total_mass": 5000.0,
            "purity": 0.95,
            "yield_rate": 0.90
        },
        "environmental_impacts": {
            "gwp": 100.0,
            "hct": 50.0,
            "frs": 75.0,
            "water_consumption": 1000.0
        },
        "resource_inputs": {
            "energy_consumption": 10000.0,
            "water_usage": 5000.0,
            "raw_material_input": 6000.0
        },
        "process_type": "RF"
    }

@pytest.mark.asyncio
async def test_calculate_eco_efficiency(process_tester, valid_eco_efficiency_request):
    """Test eco-efficiency calculation endpoint"""
    try:
        response = await process_tester.client.post(
            "/api/v1/environmental/eco-efficiency/calculate",
            json=valid_eco_efficiency_request
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "status" in data
        assert data["status"] == "success"
        assert "process_type" in data
        assert data["process_type"] == valid_eco_efficiency_request["process_type"]
        
        # Verify metrics presence
        assert "efficiency_metrics" in data
        metrics = data["efficiency_metrics"]
        assert all(key in metrics for key in [
            "economic_indicators",
            "quality_indicators",
            "efficiency_metrics"
        ])
        
        # Verify performance indicators
        assert "performance_indicators" in data
        performance = data["performance_indicators"]
        assert "eco_efficiency_index" in performance
        assert "relative_performance" in performance
        
        # Optional Rust calculations
        if "rust_calculations" in data:
            rust_calc = data["rust_calculations"]
            assert "efficiency_matrix" in rust_calc
            assert "matrix_indicators" in rust_calc
            
        logger.info("Eco-efficiency calculation test passed successfully")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_invalid_process_type(process_tester, valid_eco_efficiency_request):
    """Test validation of invalid process type"""
    invalid_request = valid_eco_efficiency_request.copy()
    invalid_request["process_type"] = "invalid_type"
    
    response = await process_tester.client.post(
        "/api/v1/environmental/eco-efficiency/calculate",
        json=invalid_request
    )
    
    assert response.status_code == 422
    error_data = response.json()
    assert "detail" in error_data

@pytest.mark.asyncio
async def test_get_efficiency_indicators(process_tester):
    """Test retrieval of efficiency indicators"""
    response = await process_tester.client.get(
        "/api/v1/environmental/eco-efficiency/indicators"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify indicator categories
    assert all(category in data for category in [
        "economic_based",
        "quality_based",
        "resource_based",
        "process_specific"
    ])
    
    # Verify specific indicators
    assert "npv_efficiency" in data["economic_based"]
    assert "purity_efficiency" in data["quality_based"]
    assert "energy_efficiency" in data["resource_based"]
    assert "baseline_reference" in data["process_specific"]

@pytest.mark.asyncio
@pytest.mark.parametrize("process_type", ["baseline", "RF", "IR"])
async def test_get_reference_values(process_tester, process_type):
    """Test retrieval of reference values for different process types"""
    response = await process_tester.client.get(
        f"/api/v1/environmental/eco-efficiency/reference-values/{process_type}"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify reference value categories
    assert all(category in data for category in [
        "economic_reference",
        "environmental_reference",
        "quality_reference"
    ])
    
    # Verify specific reference values
    assert "npv" in data["economic_reference"]
    assert "gwp" in data["environmental_reference"]
    assert "purity" in data["quality_reference"]

@pytest.mark.asyncio
async def test_invalid_reference_process_type(process_tester):
    """Test validation of invalid process type for reference values"""
    response = await process_tester.client.get(
        "/api/v1/environmental/eco-efficiency/reference-values/invalid_type"
    )
    
    assert response.status_code == 422
    error_data = response.json()
    assert "detail" in error_data

@pytest.mark.asyncio
async def test_zero_environmental_impact(process_tester, valid_eco_efficiency_request):
    """Test handling of zero environmental impact values"""
    modified_request = valid_eco_efficiency_request.copy()
    modified_request["environmental_impacts"] = {
        "gwp": 0.0,
        "hct": 0.0,
        "frs": 0.0,
        "water_consumption": 0.0
    }
    
    response = await process_tester.client.post(
        "/api/v1/environmental/eco-efficiency/calculate",
        json=modified_request
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Verify handling of potential division by zero
    if "rust_calculations" in data:
        matrix = data["rust_calculations"]["efficiency_matrix"]
        assert all(not float('inf') in str(value) for value in matrix)

@pytest.mark.asyncio
async def test_negative_values(process_tester, valid_eco_efficiency_request):
    """Test validation of negative values"""
    modified_request = valid_eco_efficiency_request.copy()
    modified_request["economic_data"]["npv"] = -1000000.0
    
    response = await process_tester.client.post(
        "/api/v1/environmental/eco-efficiency/calculate",
        json=modified_request
    )
    
    assert response.status_code == 422
    error_data = response.json()
    assert "detail" in error_data
