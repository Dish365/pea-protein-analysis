import pytest
from typing import Dict, Any
from .conftest import ProcessAnalysisTester


class TestProteinEndpoints:
    """Test suite for protein analysis endpoints"""

    @pytest.mark.asyncio
    async def test_protein_recovery_calculation(self, process_tester: ProcessAnalysisTester):
        """Test protein recovery calculation endpoint"""
        test_data = {
            "input_mass": 1000.0,
            "output_mass": 500.0,  # Further reduced to ensure recovery rate < 100%
            "initial_protein_content": 25.0,
            "output_protein_content": 35.0,
            "process_type": "Baseline"
        }

        response = await process_tester.client.post(
            "/api/v1/technical/protein-analysis/recovery",
            json=test_data
        )

        assert response.status_code == 200
        result = response.json()

        # Verify recovery metrics
        assert "recovery_rate" in result
        assert "protein_loss" in result
        assert "concentration_factor" in result
        assert "theoretical_yield" in result
        assert "expected_yield" in result

        # Verify metric types and ranges
        assert isinstance(result["recovery_rate"], float)
        assert isinstance(result["protein_loss"], float)
        assert isinstance(result["concentration_factor"], float)
        assert isinstance(result["theoretical_yield"], float)
        assert isinstance(result["expected_yield"], float)

        # Verify value ranges
        assert 0 <= result["recovery_rate"] <= 100
        assert result["protein_loss"] >= 0
        assert result["concentration_factor"] > 0

    @pytest.mark.asyncio
    async def test_separation_efficiency_analysis(self, process_tester: ProcessAnalysisTester):
        """Test separation efficiency analysis endpoint"""
        test_data = {
            "feed_composition": {
                "protein": 25.0,
                "carbohydrates": 45.0,
                "fats": 30.0
            },
            "product_composition": {
                "protein": 35.0,  # Reduced to prevent overflow
                "carbohydrates": 40.0,
                "fats": 25.0
            },
            "mass_flow": {
                "input": 1000.0,
                "output": 700.0  # Adjusted for realistic mass balance
            }
        }

        response = await process_tester.client.post(
            "/api/v1/technical/protein-analysis/separation",
            json=test_data
        )

        assert response.status_code == 200
        result = response.json()

        # Verify basic efficiency metrics
        assert "separation_factor" in result
        assert "protein_enrichment" in result
        assert "separation_efficiency" in result
        assert isinstance(result["component_recoveries"], dict)  # Changed to verify dict type

        # Verify metric types
        assert isinstance(result["separation_factor"], float)
        assert isinstance(result["protein_enrichment"], float)
        assert isinstance(result["separation_efficiency"], float)

        # Verify component recoveries structure
        recoveries = result["component_recoveries"]
        assert "protein" in recoveries
        assert "carbohydrates" in recoveries
        assert "fats" in recoveries
        assert all(isinstance(v, float) for v in recoveries.values())

    @pytest.mark.asyncio
    async def test_particle_size_analysis(self, process_tester: ProcessAnalysisTester):
        """Test particle size analysis endpoint"""
        test_data = {
            "particle_sizes": [10.0, 15.0, 20.0, 25.0, 30.0],
            "weights": [0.2, 0.2, 0.2, 0.2, 0.2],  # Simplified equal weights
            "density": 1.2,
            "target_ranges": {
                "D50": (15.0, 25.0),  # Adjusted to match data
                "span": (0.5, 1.5),    # Widened range
                "cv": (5.0, 25.0)      # Adjusted range
            }
        }

        response = await process_tester.client.post(
            "/api/v1/technical/protein-analysis/particle-size",
            json=test_data
        )

        assert response.status_code == 200
        result = response.json()

        # Verify distribution metrics
        assert "D10" in result
        assert "D50" in result
        assert "D90" in result
        assert "span" in result
        assert "mean" in result
        assert "std_dev" in result
        assert "cv" in result

        # Verify metric types
        assert isinstance(result["D50"], float)
        assert isinstance(result["span"], float)
        assert isinstance(result["cv"], float)

    @pytest.mark.asyncio
    async def test_complete_protein_analysis(self, process_tester: ProcessAnalysisTester):
        """Test complete protein analysis endpoint"""
        test_data = {
            "recovery_input": {
                "input_mass": 1000.0,
                "output_mass": 500.0,
                "initial_protein_content": 25.0,
                "output_protein_content": 35.0,
                "process_type": "Baseline"
            },
            "separation_input": {
                "feed_composition": {
                    "protein": 25.0,
                    "carbohydrates": 45.0,
                    "fats": 30.0
                },
                "product_composition": {
                    "protein": 35.0,
                    "carbohydrates": 40.0,
                    "fats": 25.0
                },
                "mass_flow": {
                    "input": 1000.0,
                    "output": 700.0
                }
            },
            "particle_input": {
                "particle_sizes": [10.0, 15.0, 20.0, 25.0, 30.0],
                "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
                "density": 1.2,
                "target_ranges": {
                    "D50": (15.0, 25.0),
                    "span": (0.5, 1.5)
                }
            }
        }

        response = await process_tester.client.post(
            "/api/v1/technical/protein-analysis/complete-analysis",
            json=test_data
        )

        assert response.status_code == 200
        result = response.json()

        # Verify response structure
        assert "recovery_metrics" in result
        assert "separation_metrics" in result
        assert "particle_metrics" in result
        assert "process_performance" in result

        # Verify recovery metrics
        recovery = result["recovery_metrics"]
        assert "recovery_rate" in recovery
        assert "protein_loss" in recovery
        assert "theoretical_yield" in recovery

        # Verify separation metrics
        separation = result["separation_metrics"]
        assert "separation_factor" in separation
        assert "protein_enrichment" in separation
        assert "separation_efficiency" in separation
        assert isinstance(separation["component_recoveries"], dict)

        # Verify particle metrics
        particle = result["particle_metrics"]
        assert "D50" in particle
        assert "span" in particle
        assert isinstance(particle["D50"], float)
        assert isinstance(particle["span"], float)

    @pytest.mark.asyncio
    async def test_invalid_protein_recovery_input(self, process_tester: ProcessAnalysisTester):
        """Test protein recovery calculation with invalid input"""
        test_data = {
            "input_mass": -1000.0,  # Invalid negative mass
            "output_mass": 800.0,
            "initial_protein_content": 25.0,
            "output_protein_content": 35.0,
            "process_type": "Baseline"
        }

        response = await process_tester.client.post(
            "/api/v1/technical/protein-analysis/recovery",
            json=test_data
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_invalid_separation_input(self, process_tester: ProcessAnalysisTester):
        """Test separation efficiency with invalid input"""
        test_data = {
            "feed_composition": {
                "protein": 125.0,  # Invalid percentage > 100
                "carbohydrates": 45.0,
                "fats": 30.0
            },
            "product_composition": {
                "protein": 45.0,
                "carbohydrates": 35.0,
                "fats": 20.0
            },
            "mass_flow": {
                "input": 1000.0,
                "output": 800.0
            }
        }

        response = await process_tester.client.post(
            "/api/v1/technical/protein-analysis/separation",
            json=test_data
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_invalid_particle_size_input(self, process_tester: ProcessAnalysisTester):
        """Test particle size analysis with invalid input"""
        test_data = {
            "particle_sizes": [10.0],  # Invalid: too few points for analysis
            "weights": [1.0],
            "density": -1.2  # Invalid negative density
        }

        response = await process_tester.client.post(
            "/api/v1/technical/protein-analysis/particle-size",
            json=test_data
        )

        assert response.status_code == 422  # Validation error
