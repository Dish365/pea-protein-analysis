import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.DEBUG)

class ProcessAnalysisTester:
    """Test suite for process analysis API endpoints"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.client = httpx.AsyncClient()
        
        # Create results directory
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)

    async def test_baseline_process(self) -> Dict[str, Any]:
        """Test baseline dry fractionation process"""
        logger.info("Testing baseline process...")
        
        baseline_data = {
            "workflow_type": "baseline",
            "process_id": "test_baseline_001",
            "analysis_type": "technical",
            "input_data": {
                "technical": {
                    "process_parameters": {
                        "feed_rate": 50.0,  # kg/h
                        "air_flow_rate": 35.0,  # m³/h
                        "classifier_speed": 3000,  # rpm
                    },
                    "material_properties": {
                        "initial_protein_content": 23.5,  # %
                        "initial_moisture": 12.0,  # %
                        "particle_size": {
                            "d10": 15.0,  # μm
                            "d50": 45.0,  # μm
                            "d90": 120.0  # μm
                        }
                    },
                    "operating_conditions": {
                        "temperature": 25.0,  # °C
                        "humidity": 45.0,  # %
                        "pressure": 1.01,  # bar
                        "processing_time": 8.0  # hours/day
                    }
                },
                "economic": {
                    "capital_costs": {
                        "equipment": {
                            "pin_mill": 45000.0,
                            "air_classifier": 75000.0,
                            "auxiliary_equipment": 25000.0
                        },
                        "installation_factor": 0.2,
                        "indirect_costs_factor": 0.15
                    },
                    "operating_costs": {
                        "utilities": {
                            "electricity_rate": 0.12,  # $/kWh
                            "electricity_consumption": 15.0  # kWh/h
                        },
                        "labor": {
                            "operators": 2,
                            "rate": 25.0  # $/h
                        },
                        "maintenance": 0.05  # % of capital cost
                    },
                    "production": {
                        "annual_capacity": 330000,  # kg/year (330 days)
                        "product_price": 2.5  # $/kg
                    }
                },
                "environmental": {
                    "energy_consumption": 15.0,  # kWh/h
                    "water_consumption": 0.0,  # m³/h
                    "waste_generation": 0.05,  # kg waste/kg product
                    "emissions": {
                        "co2": 0.5,  # kg CO2/kWh
                        "particulate_matter": 0.001  # kg/h
                    }
                }
            }
        }
        
        try:
            logger.debug(f"Sending request to {self.base_url}/pipeline/analyze")
            logger.debug(f"Request data: {json.dumps(baseline_data, indent=2)}")
            response = await self.client.post(
                f"{self.base_url}/pipeline/analyze",
                json=baseline_data,
                timeout=30.0
            )
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response content: {response.text}")
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                raise Exception(f"Baseline process analysis failed: {error_detail}")
                
            results = response.json()
            self._save_results("baseline_results.json", results)
            return results
            
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Baseline process analysis failed: {str(e)}")

    async def test_rf_treatment_process(self) -> Dict[str, Any]:
        """Test RF treatment process"""
        logger.info("Testing RF treatment process...")
        
        rf_data = {
            "workflow_type": "rf_treatment",
            "process_id": "test_rf_001",
            "analysis_type": "technical",
            "input_data": {
                "technical": {
                    "pretreatment": {
                        "rf_power": 3.0,  # kW
                        "frequency": 27.12,  # MHz
                        "treatment_time": 5.0,  # minutes
                        "energy_efficiency": 0.85
                    },
                    "process_parameters": {
                        "feed_rate": 45.0,  # kg/h
                        "air_flow_rate": 35.0,  # m³/h
                        "classifier_speed": 3000  # rpm
                    },
                    "material_properties": {
                        "initial_protein_content": 23.5,  # %
                        "initial_moisture": 12.0,  # %
                        "dielectric_properties": {
                            "dielectric_constant": 2.8,
                            "loss_factor": 0.15
                        }
                    }
                },
                "economic": {
                    "capital_costs": {
                        "equipment": {
                            "rf_generator": 120000.0,
                            "pin_mill": 45000.0,
                            "air_classifier": 75000.0,
                            "auxiliary_equipment": 30000.0
                        },
                        "installation_factor": 0.25,
                        "indirect_costs_factor": 0.18
                    },
                    "operating_costs": {
                        "utilities": {
                            "electricity_rate": 0.12,  # $/kWh
                            "electricity_consumption": 25.0  # kWh/h
                        },
                        "labor": {
                            "operators": 2,
                            "rate": 25.0  # $/h
                        },
                        "maintenance": 0.06  # % of capital cost
                    },
                    "production": {
                        "annual_capacity": 297000,  # kg/year (330 days)
                        "product_price": 2.8  # $/kg
                    }
                }
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/pipeline/analyze",
                json=rf_data,
                timeout=30.0
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                raise Exception(f"RF treatment analysis failed: {error_detail}")
                
            results = response.json()
            self._save_results("rf_treatment_results.json", results)
            return results
            
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"RF treatment analysis failed: {str(e)}")

    async def test_ir_treatment_process(self) -> Dict[str, Any]:
        """Test IR treatment process"""
        logger.info("Testing IR treatment process...")
        
        ir_data = {
            "workflow_type": "ir_treatment",
            "process_id": "test_ir_001",
            "analysis_type": "technical",
            "input_data": {
                "technical": {
                    "ir_parameters": {
                        "power_density": 5.0,  # kW/m²
                        "wavelength": 3.4,  # μm
                        "treatment_time": 3.0  # minutes
                    },
                    "material_properties": {
                        "initial_moisture": 12.0,
                        "surface_temperature": 90.0,  # °C
                        "layer_thickness": 2.0  # mm
                    },
                    "process_conditions": {
                        "temperature": 25.0,
                        "humidity": 45.0,
                        "pressure": 1.01
                    },
                    "fractionation": {
                        "feed_rate": 48.0,
                        "air_flow_rate": 35.0,
                        "classifier_speed": 3000
                    }
                },
                "economic": {
                    "equipment_costs": {
                        "ir_heater": 85000.0,
                        "classifier": 75000.0,
                        "mill": 45000.0,
                        "auxiliary": 28000.0
                    },
                    "operating_costs": {
                        "electricity_rate": 0.12,
                        "labor_rate": 25.0,
                        "maintenance_factor": 0.055
                    },
                    "production_scale": 1000.0
                }
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/pipeline/analyze",
                json=ir_data,
                timeout=30.0
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                raise Exception(f"IR treatment analysis failed: {error_detail}")
                
            results = response.json()
            self._save_results("ir_treatment_results.json", results)
            return results
            
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"IR treatment analysis failed: {str(e)}")

    async def compare_processes(self, results: Dict[str, Dict[str, Any]]) -> None:
        """Compare results between processes"""
        logger.info("Comparing process results...")
        
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "technical_comparison": {
                "protein_yield": {
                    "baseline": results["baseline"]["technical"]["protein_yield"],
                    "rf_treatment": results["rf_treatment"]["technical"]["protein_yield"],
                    "ir_treatment": results["ir_treatment"]["technical"]["protein_yield"]
                },
                "separation_efficiency": {
                    "baseline": results["baseline"]["technical"]["separation_efficiency"],
                    "rf_treatment": results["rf_treatment"]["technical"]["separation_efficiency"],
                    "ir_treatment": results["ir_treatment"]["technical"]["separation_efficiency"]
                }
            },
            "economic_comparison": {
                "capex": {
                    "baseline": results["baseline"]["economic"]["capex"],
                    "rf_treatment": results["rf_treatment"]["economic"]["capex"],
                    "ir_treatment": results["ir_treatment"]["economic"]["capex"]
                },
                "opex": {
                    "baseline": results["baseline"]["economic"]["opex"],
                    "rf_treatment": results["rf_treatment"]["economic"]["opex"],
                    "ir_treatment": results["ir_treatment"]["economic"]["opex"]
                },
                "npv": {
                    "baseline": results["baseline"]["economic"]["npv"],
                    "rf_treatment": results["rf_treatment"]["economic"]["npv"],
                    "ir_treatment": results["ir_treatment"]["economic"]["npv"]
                }
            },
            "environmental_comparison": {
                "gwp": {
                    "baseline": results["baseline"]["environmental"]["gwp"],
                    "rf_treatment": results["rf_treatment"]["environmental"]["gwp"],
                    "ir_treatment": results["ir_treatment"]["environmental"]["gwp"]
                },
                "energy_consumption": {
                    "baseline": results["baseline"]["environmental"]["energy_consumption"],
                    "rf_treatment": results["rf_treatment"]["environmental"]["energy_consumption"],
                    "ir_treatment": results["ir_treatment"]["environmental"]["energy_consumption"]
                }
            }
        }
        
        self._save_results("process_comparison.json", comparison)
        logger.info("Comparison results saved")

    def _save_results(self, filename: str, data: Dict[str, Any]) -> None:
        """Save results to JSON file"""
        file_path = self.results_dir / filename
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Results saved to {file_path}")

async def main():
    """Main test execution"""
    tester = ProcessAnalysisTester()
    
    try:
        # Run process tests
        results = {
            "baseline": await tester.test_baseline_process(),
            "rf_treatment": await tester.test_rf_treatment_process(),
            "ir_treatment": await tester.test_ir_treatment_process()
        }
        
        # Compare results
        await tester.compare_processes(results)
        logger.info("All tests completed successfully")
        
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
    finally:
        await tester.client.aclose()

if __name__ == "__main__":
    asyncio.run(main()) 