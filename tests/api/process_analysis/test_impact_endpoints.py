import pytest
from fastapi.testclient import TestClient
from backend.fastapi_app.main import app
from typing import Dict, Any
from .conftest import ProcessAnalysisTester
import math

client = TestClient(app)

# Test data fixtures
@pytest.fixture
def valid_process_data() -> Dict:
    return {
        "electricity_kwh": 1000.0,
        "water_kg": 500.0,
        "transport_ton_km": 200.0,
        "product_kg": 100.0,
        "equipment_kg": 50.0,
        "cooling_kwh": 300.0,
        "waste_kg": 75.0,
        "thermal_ratio": 0.3  # Adding default thermal ratio
    }

@pytest.fixture
def expected_impact_categories() -> set:
    return {"gwp", "hct", "frs", "water_consumption"}

class TestEnvironmentalEndpoints:
    """Test suite for environmental impact endpoints"""
    
    @pytest.mark.asyncio
    async def test_calculate_impacts_success(self, process_tester: ProcessAnalysisTester):
        """Test successful impact calculation with valid process data"""
        test_data = {
            "electricity_kwh": 1000.0,
            "water_kg": 500.0,
            "transport_ton_km": 200.0,
            "product_kg": 100.0,
            "equipment_kg": 50.0,
            "cooling_kwh": 300.0,
            "waste_kg": 75.0,
            "thermal_ratio": 0.3
        }
        
        response = await process_tester.client.post(
            "/api/v1/environmental/impact/calculate-impacts",
            json=test_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # Check response structure
        assert "status" in result
        assert result["status"] == "success"
        assert "impacts" in result
        assert "process_contributions" in result
        
        # Validate impact metrics
        impacts = result["impacts"]
        assert isinstance(impacts, dict)
        assert all(metric in impacts for metric in ["gwp", "hct", "frs", "water_consumption"])
        assert all(isinstance(value, (int, float)) for value in impacts.values())
        
        # Validate process contributions
        contributions = result["process_contributions"]
        assert isinstance(contributions, dict)
        assert all(metric in contributions for metric in ["gwp", "hct", "frs", "water"])
        assert all(isinstance(contrib, dict) for contrib in contributions.values())

    @pytest.mark.asyncio
    async def test_get_impact_factors(self, process_tester: ProcessAnalysisTester):
        """Test retrieving environmental impact factors"""
        response = await process_tester.client.get(
            "/api/v1/environmental/impact/impact-factors"
        )
        
        assert response.status_code == 200
        factors = response.json()
        
        # Verify all factor categories are present
        assert all(key in factors for key in [
            "gwp_factors",
            "hct_factors", 
            "frs_factors",
            "water_factors"
        ])
        
        # Verify factor structure
        for factor_category in factors.values():
            assert isinstance(factor_category, dict)
            assert len(factor_category) > 0
            assert all(isinstance(k, str) and isinstance(v, (int, float)) 
                      for k, v in factor_category.items())

    @pytest.mark.asyncio
    async def test_process_contributions(self, process_tester: ProcessAnalysisTester):
        """Test process contributions calculation"""
        test_data = {
            "electricity_kwh": 1000.0,
            "water_kg": 500.0,
            "transport_ton_km": 200.0,
            "product_kg": 100.0,
            "equipment_kg": 50.0,
            "cooling_kwh": 300.0,
            "waste_kg": 75.0,
            "thermal_ratio": 0.5  # Equal split between thermal and mechanical
        }
        
        response = await process_tester.client.post(
            "/api/v1/environmental/impact/calculate-impacts",
            json=test_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # Verify contributions structure
        contributions = result["process_contributions"]
        
        # Check GWP contributions
        assert "electricity" in contributions["gwp"]
        assert "water" in contributions["gwp"]
        assert "transport" in contributions["gwp"]
        
        # Check HCT contributions
        assert "electricity" in contributions["hct"]
        assert "water_treatment" in contributions["hct"]
        assert "waste" in contributions["hct"]
        
        # Check FRS contributions
        assert "electricity" in contributions["frs"]
        assert "thermal_treatment" in contributions["frs"]
        assert "mechanical_processing" in contributions["frs"]
        
        # Check Water contributions
        assert "tempering" in contributions["water"]
        assert "cleaning" in contributions["water"]
        assert "cooling" in contributions["water"]

    @pytest.mark.asyncio
    async def test_calculation_consistency(self, process_tester: ProcessAnalysisTester):
        """Test consistency of impact calculations"""
        test_data = {
            "electricity_kwh": 1000.0,
            "water_kg": 500.0,
            "transport_ton_km": 200.0,
            "product_kg": 100.0,
            "equipment_kg": 50.0,
            "cooling_kwh": 300.0,
            "waste_kg": 75.0,
            "thermal_ratio": 0.3
        }
        
        # Make multiple requests with the same data
        responses = []
        for _ in range(3):
            response = await process_tester.client.post(
                "/api/v1/environmental/impact/calculate-impacts",
                json=test_data
            )
            assert response.status_code == 200
            responses.append(response.json())
        
        # Verify all responses are identical
        first_response = responses[0]
        for response in responses[1:]:
            assert response["impacts"] == first_response["impacts"]
            assert response["process_contributions"] == first_response["process_contributions"]

    @pytest.mark.asyncio
    async def test_impact_factors_error_handling(self, process_tester: ProcessAnalysisTester):
        """Test error handling in impact factors endpoint"""
        # Simulate server error by sending invalid accept header
        response = await process_tester.client.get(
            "/api/v1/environmental/impact/impact-factors",
            headers={"Accept": "invalid/type"}
        )
        assert response.status_code in (400, 406)

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, process_tester: ProcessAnalysisTester, valid_process_data: Dict):
        """Test handling of concurrent requests"""
        import asyncio
        
        # Create multiple concurrent requests
        tasks = [
            process_tester.client.post(
                "/api/v1/environmental/impact/calculate-impacts",
                json=valid_process_data
            ) for _ in range(5)
        ]
        
        # Wait for all requests to complete
        responses = await asyncio.gather(*tasks)
        
        # Verify all requests succeeded
        assert all(r.status_code == 200 for r in responses)
        
        # Verify all responses are consistent
        first_response = responses[0].json()
        for response in responses[1:]:
            assert response.json() == first_response

    @pytest.mark.asyncio
    async def test_malformed_json(self, process_tester: ProcessAnalysisTester):
        """Test handling of malformed JSON input"""
        response = await process_tester.client.post(
            "/api/v1/environmental/impact/calculate-impacts",
            content=b"invalid json{",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_wrong_content_type(self, process_tester: ProcessAnalysisTester, valid_process_data: Dict):
        """Test handling of wrong content type"""
        response = await process_tester.client.post(
            "/api/v1/environmental/impact/calculate-impacts",
            content=str(valid_process_data).encode(),
            headers={"Content-Type": "text/plain"}
        )
        assert response.status_code in (415, 422)

    @pytest.mark.asyncio
    async def test_calculate_and_allocate(self, process_tester: ProcessAnalysisTester, valid_process_data: Dict):
        """Test combined impact calculation and allocation"""
        allocation_request = {
            "product_values": {"product1": 10.0, "product2": 5.0},
            "mass_flows": {"product1": 60.0, "product2": 40.0},
            "method": "hybrid",
            "hybrid_weights": {"economic": 0.6, "physical": 0.4}
        }

        response = await process_tester.client.post(
            "/api/v1/environmental/impact/calculate-and-allocate",
            json={
                "data": valid_process_data,
                "allocation_request": allocation_request
            }
        )

        assert response.status_code == 200
        result = response.json()

        # Verify response structure
        assert "status" in result
        assert result["status"] == "success"
        assert "impact_results" in result
        assert "allocation_results" in result

        # Verify impact results
        impact_results = result["impact_results"]
        assert "impacts" in impact_results
        assert "process_contributions" in impact_results

        # Verify allocation results
        allocation_results = result["allocation_results"]
        assert "allocation_factors" in allocation_results
        assert "allocated_impacts" in allocation_results

    @pytest.mark.asyncio
    async def test_allocation_methods(self, process_tester: ProcessAnalysisTester):
        """Test different allocation methods"""
        response = await process_tester.client.get(
            "/api/v1/environmental/allocation/methods"
        )

        assert response.status_code == 200
        methods = response.json()

        # Verify all allocation methods are present
        assert "economic" in methods
        assert "physical" in methods
        assert "hybrid" in methods

    @pytest.mark.asyncio
    async def test_allocation_calculation(self, process_tester: ProcessAnalysisTester):
        """Test standalone allocation calculation"""
        allocation_request = {
            "impacts": {"gwp": 100.0, "hct": 50.0},
            "product_values": {"product1": 10.0, "product2": 5.0},
            "mass_flows": {"product1": 60.0, "product2": 40.0},
            "method": "hybrid",
            "hybrid_weights": {"economic": 0.6, "physical": 0.4}
        }

        response = await process_tester.client.post(
            "/api/v1/environmental/allocation/calculate",
            json=allocation_request
        )

        assert response.status_code == 200
        result = response.json()

        # Verify allocation results
        assert "status" in result
        assert result["status"] == "success"
        assert "method" in result
        assert "results" in result

        # Verify allocation factors sum to approximately 1
        factors = result["results"]["allocation_factors"]
        assert math.isclose(sum(factors.values()), 1.0, rel_tol=1e-9)

    @pytest.mark.asyncio
    async def test_invalid_allocation_request(self, process_tester: ProcessAnalysisTester):
        """Test allocation with invalid request data"""
        invalid_request = {
            "impacts": {"gwp": -100.0},  # Invalid negative impact
            "product_values": {"product1": 10.0},
            "mass_flows": {"product1": 60.0, "product2": 40.0},  # Mismatched products
            "method": "invalid_method"  # Invalid method
        }

        response = await process_tester.client.post(
            "/api/v1/environmental/allocation/calculate",
            json=invalid_request
        )

        assert response.status_code == 422  # Validation error

class TestCombinedEndpoints:
    """Test suite for combined impact and allocation endpoints"""
    
    @pytest.mark.asyncio
    async def test_calculate_and_allocate(self, process_tester: ProcessAnalysisTester, valid_process_data: Dict):
        """Test combined impact calculation and allocation"""
        allocation_request = {
            "product_values": {"product1": 10.0, "product2": 5.0},
            "mass_flows": {"product1": 60.0, "product2": 40.0},
            "method": "hybrid",
            "hybrid_weights": {"economic": 0.6, "physical": 0.4}
        }

        response = await process_tester.client.post(
            "/api/v1/environmental/impact/calculate-and-allocate",
            json={
                "data": valid_process_data,
                "allocation_request": allocation_request
            }
        )

        assert response.status_code == 200
        result = response.json()

        # Verify response structure
        assert "status" in result
        assert result["status"] == "success"
        assert "impact_results" in result
        assert "allocation_results" in result

        # Verify impact results
        impact_results = result["impact_results"]
        assert "impacts" in impact_results
        assert "process_contributions" in impact_results

        # Verify allocation results
        allocation_results = result["allocation_results"]
        assert "allocation_factors" in allocation_results
        assert "allocated_impacts" in allocation_results

class TestAllocationEndpoints:
    """Test suite for allocation endpoints"""

    @pytest.mark.asyncio
    async def test_allocation_methods(self, process_tester: ProcessAnalysisTester):
        """Test different allocation methods"""
        response = await process_tester.client.get(
            "/api/v1/environmental/allocation/methods"
        )

        assert response.status_code == 200
        methods = response.json()

        # Verify all allocation methods are present
        assert "economic" in methods
        assert "physical" in methods
        assert "hybrid" in methods

    @pytest.mark.asyncio
    async def test_allocation_calculation(self, process_tester: ProcessAnalysisTester):
        """Test standalone allocation calculation"""
        allocation_request = {
            "impacts": {"gwp": 100.0, "hct": 50.0},
            "product_values": {"product1": 10.0, "product2": 5.0},
            "mass_flows": {"product1": 60.0, "product2": 40.0},
            "method": "hybrid",
            "hybrid_weights": {"economic": 0.6, "physical": 0.4}
        }

        response = await process_tester.client.post(
            "/api/v1/environmental/allocation/calculate",
            json=allocation_request
        )

        assert response.status_code == 200
        result = response.json()

        # Verify allocation results
        assert "status" in result
        assert result["status"] == "success"
        assert "method" in result
        assert "results" in result

        # Verify allocation factors sum to approximately 1
        factors = result["results"]["allocation_factors"]
        assert math.isclose(sum(factors.values()), 1.0, rel_tol=1e-9)

    @pytest.mark.asyncio
    async def test_invalid_allocation_request(self, process_tester: ProcessAnalysisTester):
        """Test allocation with invalid request data"""
        invalid_request = {
            "impacts": {"gwp": -100.0},  # Invalid negative impact
            "product_values": {"product1": 10.0},
            "mass_flows": {"product1": 60.0, "product2": 40.0},  # Mismatched products
            "method": "invalid_method"  # Invalid method
        }

        response = await process_tester.client.post(
            "/api/v1/environmental/allocation/calculate",
            json=invalid_request
        )

        assert response.status_code == 422  # Validation error
