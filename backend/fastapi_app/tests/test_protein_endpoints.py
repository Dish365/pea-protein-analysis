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
