import pytest
from fastapi.testclient import TestClient
import numpy as np


def test_protein_recovery(client, protein_recovery_data):
    response = client.post(
        "/protein-analysis/recovery/", json=protein_recovery_data
    )
    assert response.status_code == 200

    data = response.json()
    assert "recovery_rate" in data
    assert "protein_loss" in data
    assert "concentration_factor" in data
    assert "theoretical_yield" in data
    assert "expected_yield" in data

    # Verify calculations
    assert 0 <= data["recovery_rate"] <= 100
    assert data["concentration_factor"] > 1


def test_separation_efficiency(client, separation_efficiency_data):
    response = client.post(
        "/protein-analysis/separation/", json=separation_efficiency_data
    )
    assert response.status_code == 200

    data = response.json()
    assert "separation_factor" in data
    assert "protein_enrichment" in data
    assert "separation_efficiency" in data
    assert "cumulative_efficiency" in data
    assert "average_step_efficiency" in data

    # Verify calculations
    assert data["separation_factor"] > 1
    assert data["protein_enrichment"] > 0


def test_particle_size_analysis(client, particle_size_data):
    response = client.post("/protein-analysis/particle-size/", json=particle_size_data)
    assert response.status_code == 200

    data = response.json()
    # Check Rust-calculated metrics
    assert "D10" in data
    assert "D50" in data
    assert "D90" in data
    assert "mean" in data
    assert "std_dev" in data
    assert "span" in data
    assert "cv" in data

    # Verify calculations from Rust
    assert data["D10"] < data["D50"] < data["D90"]
    assert data["span"] > 0
    assert data["cv"] > 0

    # If density was provided, check surface area calculations
    if "density" in particle_size_data:
        assert "specific_surface_area" in data
        assert "total_surface_area" in data
        assert "mean_surface_area" in data
        assert data["specific_surface_area"] > 0

    # If target ranges were provided, check quality scores
    if "target_ranges" in particle_size_data:
        for param in particle_size_data["target_ranges"]:
            assert f"{param}_quality" in data
        assert "overall_quality" in data
        assert all(0 <= score <= 100 for score in data.values() if isinstance(score, float))


def test_complete_analysis(
    client, protein_recovery_data, separation_efficiency_data, particle_size_data
):
    response = client.post(
        "/protein-analysis/complete-analysis/",
        json={
            "recovery_input": protein_recovery_data,
            "separation_input": separation_efficiency_data,
            "particle_input": particle_size_data,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "recovery_metrics" in data
    assert "separation_metrics" in data
    assert "particle_metrics" in data
    assert "process_performance" in data

    # Verify Rust-calculated particle metrics
    particle_metrics = data["particle_metrics"]
    assert particle_metrics["D10"] < particle_metrics["D50"] < particle_metrics["D90"]
    assert particle_metrics["span"] > 0
    assert particle_metrics["cv"] > 0


@pytest.fixture
def particle_size_data():
    """Sample particle size data for testing"""
    return {
        "particle_sizes": [10.0, 15.0, 20.0, 25.0, 30.0],
        "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
        "density": 1.2,
        "target_ranges": {
            "D50": (15.0, 25.0),
            "span": (0.5, 1.5)
        }
    }


def test_invalid_protein_recovery_input(client):
    invalid_data = {
        "input_mass": -100.0,  # Invalid negative mass
        "output_mass": 25.0,
        "initial_protein_content": 120.0,  # Invalid percentage > 100
        "output_protein_content": 65.0,
        "process_type": "baseline",
    }
    response = client.post("/protein-analysis/recovery/", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_invalid_separation_efficiency_input(client):
    invalid_data = {
        "feed_composition": {},  # Missing required components
        "product_composition": {},
        "mass_flow": {"input": -100.0},  # Invalid negative mass flow
    }
    response = client.post(
        "/protein-analysis/separation/", json=invalid_data
    )
    assert response.status_code == 422  # Validation error


def test_invalid_particle_size_input(client):
    """Test invalid particle size inputs"""
    # Test empty particle sizes
    invalid_data = {
        "particle_sizes": [],
        "weights": [],
    }
    response = client.post("/protein-analysis/particle-size/", json=invalid_data)
    assert response.status_code == 422

    # Test mismatched weights length
    invalid_data = {
        "particle_sizes": [10.0, 20.0, 30.0],
        "weights": [0.5, 0.5],  # Wrong length
    }
    response = client.post("/protein-analysis/particle-size/", json=invalid_data)
    assert response.status_code == 422

    # Test invalid weights sum
    invalid_data = {
        "particle_sizes": [10.0, 20.0, 30.0],
        "weights": [0.5, 0.5, 0.5],  # Sum > 1
    }
    response = client.post("/protein-analysis/particle-size/", json=invalid_data)
    assert response.status_code == 422

    # Test negative particle sizes
    invalid_data = {
        "particle_sizes": [-10.0, 20.0, 30.0],
        "weights": [0.3, 0.3, 0.4],
    }
    response = client.post("/protein-analysis/particle-size/", json=invalid_data)
    assert response.status_code == 422


def test_rust_particle_analysis_accuracy(client):
    """Test accuracy of Rust-calculated particle size metrics"""
    # Generate test data
    sizes = np.linspace(10, 100, 1000)  # 1000 points between 10 and 100
    weights = np.ones_like(sizes) / len(sizes)  # Uniform weights
    
    test_data = {
        "particle_sizes": sizes.tolist(),
        "weights": weights.tolist(),
    }
    
    response = client.post("/protein-analysis/particle-size/", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify statistical properties
    assert abs(data["D50"] - np.median(sizes)) < 1e-6  # Median should match
    assert abs(data["mean"] - np.mean(sizes)) < 1e-6  # Mean should match
    assert abs(data["std_dev"] - np.std(sizes)) < 1e-6  # Standard deviation should match


def test_separation_efficiency_caching(client, separation_efficiency_data):
    """Test that separation efficiency calculations are properly cached"""
    # First call
    response1 = client.post(
        "/protein-analysis/separation/", json=separation_efficiency_data
    )
    assert response1.status_code == 200
    data1 = response1.json()

    # Second call with same data should use cache
    response2 = client.post(
        "/protein-analysis/separation/", json=separation_efficiency_data
    )
    assert response2.status_code == 200
    data2 = response2.json()

    # Results should be identical
    assert data1 == data2

    # Modify input slightly
    modified_data = separation_efficiency_data.copy()
    modified_data["mass_flow"]["input"] += 1.0

    # Call with modified data should calculate new results
    response3 = client.post(
        "/protein-analysis/separation/", json=modified_data
    )
    assert response3.status_code == 200
    data3 = response3.json()

    # Results should be different
    assert data1 != data3


def test_separation_efficiency_process_performance(client, separation_efficiency_data):
    """Test process performance analysis with multi-stage data"""
    response = client.post(
        "/protein-analysis/separation/", json=separation_efficiency_data
    )
    assert response.status_code == 200
    data = response.json()

    # Check process performance metrics
    assert "cumulative_efficiency" in data
    assert "average_step_efficiency" in data
    assert "purity_achievement" in data
    assert 0 <= data["cumulative_efficiency"] <= 100
    assert 0 <= data["average_step_efficiency"] <= 100
    assert 0 <= data["purity_achievement"] <= 100

    # Check stage analysis
    assert "stage_analysis" in data
    stage_analysis = data["stage_analysis"]
    assert "enrichment_contributions" in stage_analysis
    assert "efficiency_ratios" in stage_analysis
    assert "bottleneck_scores" in stage_analysis
    assert len(stage_analysis["enrichment_contributions"]) == len(separation_efficiency_data["process_data"])


def test_separation_efficiency_validation_errors(client):
    """Test various validation error cases for separation efficiency"""
    # Test missing protein in composition
    invalid_data = {
        "feed_composition": {"starch": 60.0, "fiber": 40.0},  # Missing protein
        "product_composition": {"protein": 65.0, "starch": 20.0, "fiber": 15.0},
        "mass_flow": {"input": 100.0, "output": 25.0}
    }
    response = client.post("/protein-analysis/separation/", json=invalid_data)
    assert response.status_code == 422
    assert "error" in response.json()
    assert response.json()["type"] == "ValueError"

    # Test composition not summing to 100%
    invalid_data = {
        "feed_composition": {"protein": 20.0, "starch": 45.0, "fiber": 45.0},  # Sums to 110%
        "product_composition": {"protein": 65.0, "starch": 20.0, "fiber": 15.0},
        "mass_flow": {"input": 100.0, "output": 25.0}
    }
    response = client.post("/protein-analysis/separation/", json=invalid_data)
    assert response.status_code == 422
    assert "error" in response.json()
    assert "sum to 100%" in response.json()["message"].lower()

    # Test invalid mass flow
    invalid_data = {
        "feed_composition": {"protein": 20.0, "starch": 45.0, "fiber": 35.0},
        "product_composition": {"protein": 65.0, "starch": 20.0, "fiber": 15.0},
        "mass_flow": {"input": 100.0, "output": 150.0}  # Output > Input
    }
    response = client.post("/protein-analysis/separation/", json=invalid_data)
    assert response.status_code == 422
    assert "error" in response.json()
    assert "output mass cannot" in response.json()["message"].lower()


def test_separation_efficiency_process_errors(client, separation_efficiency_data):
    """Test error handling in process performance analysis"""
    # Test invalid target purity
    invalid_data = separation_efficiency_data.copy()
    invalid_data["target_purity"] = -10.0
    response = client.post("/protein-analysis/separation/", json=invalid_data)
    assert response.status_code == 422
    assert "error" in response.json()
    assert "target purity" in response.json()["message"].lower()

    # Test inconsistent process data
    invalid_data = separation_efficiency_data.copy()
    invalid_data["process_data"] = [
        {
            "feed": {"protein": 20.0},
            "product": {"protein": 40.0},
            "mass_flow": {"input": 100.0, "output": 45.0}
        },
        {
            "feed": {"protein": 50.0},  # Inconsistent with previous stage
            "product": {"protein": 65.0},
            "mass_flow": {"input": 45.0, "output": 25.0}
        }
    ]
    response = client.post("/protein-analysis/separation/", json=invalid_data)
    assert response.status_code == 422
    assert "error" in response.json()
    assert "process performance" in response.json()["error"].lower()
