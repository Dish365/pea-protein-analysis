import pytest
from fastapi.testclient import TestClient

def test_protein_recovery(client, protein_recovery_data):
    response = client.post("/process/technical/protein-recovery/", json=protein_recovery_data)
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
        "/process/technical/separation-efficiency/",
        json=separation_efficiency_data
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
    response = client.post("/process/technical/particle-size/", json=particle_size_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "D10" in data
    assert "D50" in data
    assert "D90" in data
    assert "span" in data
    assert "mean" in data
    assert "std_dev" in data
    assert "specific_surface_area" in data
    
    # Verify calculations
    assert data["D10"] < data["D50"] < data["D90"]
    assert data["span"] > 0

def test_complete_analysis(
    client, 
    protein_recovery_data, 
    separation_efficiency_data, 
    particle_size_data
):
    response = client.post(
        "/process/technical/complete-analysis/",
        json={
            "recovery_input": protein_recovery_data,
            "separation_input": separation_efficiency_data,
            "particle_input": particle_size_data
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "recovery_metrics" in data
    assert "separation_metrics" in data
    assert "particle_metrics" in data
    assert "process_performance" in data

def test_invalid_protein_recovery_input(client):
    invalid_data = {
        "input_mass": -100.0,  # Invalid negative mass
        "output_mass": 25.0,
        "initial_protein_content": 120.0,  # Invalid percentage > 100
        "output_protein_content": 65.0,
        "process_type": "baseline"
    }
    response = client.post("/process/technical/protein-recovery/", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_invalid_separation_efficiency_input(client):
    invalid_data = {
        "feed_composition": {},  # Missing required components
        "product_composition": {},
        "mass_flow": {"input": -100.0}  # Invalid negative mass flow
    }
    response = client.post("/process/technical/separation-efficiency/", json=invalid_data)
    assert response.status_code == 422  # Validation error 