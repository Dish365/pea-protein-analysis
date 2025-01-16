import pytest
from fastapi.testclient import TestClient
from backend.fastapi_app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def protein_recovery_data():
    return {
        "input_mass": 100.0,
        "output_mass": 25.0,
        "initial_protein_content": 20.0,
        "output_protein_content": 65.0,
        "process_type": "baseline",
    }


@pytest.fixture
def separation_efficiency_data():
    return {
        "feed_composition": {"protein": 20.0, "starch": 45.0, "fiber": 35.0},
        "product_composition": {"protein": 65.0, "starch": 20.0, "fiber": 15.0},
        "mass_flow": {"input": 100.0, "output": 25.0},
        "process_data": [
            {
                "feed": {"protein": 20.0},
                "product": {"protein": 40.0},
                "mass_flow": {"input": 100.0, "output": 45.0},
            },
            {
                "feed": {"protein": 40.0},
                "product": {"protein": 65.0},
                "mass_flow": {"input": 45.0, "output": 25.0},
            },
        ],
        "target_purity": 70.0,
    }


@pytest.fixture
def particle_size_data():
    return {
        "particle_sizes": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0],
        "weights": [
            0.05,
            0.1,
            0.15,
            0.2,
            0.2,
            0.1,
            0.08,
            0.05,
            0.05,
            0.02,
        ],  # Sum = 1.0
        "density": 1.3,
        "target_ranges": {"D50": (20.0, 30.0), "span": (0.8, 1.2)},
    }
