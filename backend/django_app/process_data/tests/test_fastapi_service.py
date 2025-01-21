import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from process_data.services.fastapi_service import FastAPIService
import httpx
import tenacity
from django.conf import settings

pytestmark = pytest.mark.django_db

@pytest.mark.asyncio
class TestFastAPIService:
    @pytest.fixture
    def service(self):
        """FastAPI service instance"""
        return FastAPIService()
    
    @pytest.fixture
    def mock_httpx_client(self):
        """Mock httpx client"""
        with patch('httpx.AsyncClient', autospec=True) as mock_client:
            client_instance = mock_client.return_value
            client_instance.post = AsyncMock()
            client_instance.aclose = AsyncMock()
            yield client_instance
    
    @pytest.fixture
    def mock_integrators(self):
        """Mock all integrators"""
        with patch('analytics.pipeline.integrator.technical.TechnicalIntegrator') as mock_tech, \
             patch('analytics.pipeline.integrator.economic.EconomicIntegrator') as mock_econ, \
             patch('analytics.pipeline.integrator.environmental.EnvironmentalIntegrator') as mock_env:
            
            # Configure technical integrator
            tech_instance = mock_tech.return_value
            tech_instance.analyze_technical = AsyncMock(return_value={
                "technical_results": {
                    "protein_recovery": 0.8,
                    "separation_efficiency": 0.85,
                    "process_efficiency": 0.75,
                    "particle_size_distribution": {"d10": 10.0, "d50": 50.0, "d90": 90.0}
                }
            })
            tech_instance.analyze_protein_recovery = AsyncMock(return_value={
                "protein_recovery": 0.8,
                "mass_balance": {"input": 100.0, "output": 80.0}
            })
            tech_instance.analyze_separation_efficiency = AsyncMock(return_value={
                "separation_efficiency": 0.85,
                "process_efficiency": 0.75
            })
            tech_instance.client = AsyncMock()
            tech_instance.client.post = AsyncMock()
            tech_instance.client.post.return_value.status_code = 200
            tech_instance.client.post.return_value.json = AsyncMock(return_value={
                "protein_recovery": 0.8,
                "separation_efficiency": 0.85
            })
            tech_instance.client.aclose = AsyncMock()
            
            # Configure economic integrator
            econ_instance = mock_econ.return_value
            econ_instance.analyze_economics = AsyncMock(return_value={
                "capex_analysis": {
                    "summary": {
                        "equipment_costs": 50000.0,
                        "installation_costs": 10000.0,
                        "indirect_costs": 7500.0,
                        "total_capex": 67500.0
                    },
                    "equipment_breakdown": [{
                        "name": "main_equipment",
                        "cost": 50000.0,
                        "installation_cost": 10000.0,
                        "indirect_cost": 7500.0
                    }],
                    "process_type": "baseline"
                },
                "opex_analysis": {
                    "summary": {
                        "utilities_cost": 5000.0,
                        "materials_cost": 3000.0,
                        "labor_cost": 5000.0,
                        "maintenance_cost": 2000.0,
                        "total_opex": 15000.0
                    },
                    "utilities_breakdown": [],
                    "raw_materials_breakdown": [],
                    "labor_breakdown": {},
                    "process_type": "baseline"
                },
                "profitability_analysis": {
                    "metrics": {
                        "npv": 250000.0,
                        "roi": 0.25,
                        "payback_period": 3.5,
                        "profitability_index": 1.8
                    },
                    "monte_carlo": None,
                    "cash_flows": [-67500.0, 25000.0, 25000.0, 25000.0, 25000.0]
                },
                "economic_analysis": {
                    "investment_analysis": {},
                    "annual_costs": {},
                    "profitability_metrics": {}
                },
                "sensitivity_analysis": {"sensitivity_analysis": {}},
                "cost_tracking": {
                    "summary": {"cost_summary": {}},
                    "trends": {"cost_trends": []}
                }
            })
            econ_instance.calculate_capex = AsyncMock(return_value={
                "capex_summary": {
                    "equipment_costs": 50000.0,
                    "installation_costs": 10000.0,
                    "indirect_costs": 7500.0,
                    "total_capex": 67500.0
                },
                "equipment_breakdown": [{
                    "name": "main_equipment",
                    "cost": 50000.0,
                    "installation_cost": 10000.0,
                    "indirect_cost": 7500.0
                }],
                "process_type": "baseline"
            })
            econ_instance.client = AsyncMock()
            econ_instance.client.post = AsyncMock()
            econ_instance.client.post.return_value.status_code = 200
            econ_instance.client.post.return_value.json = AsyncMock(return_value={
                "capex_summary": {
                    "equipment_costs": 50000.0,
                    "installation_costs": 10000.0,
                    "indirect_costs": 7500.0,
                    "total_capex": 67500.0
                }
            })
            econ_instance.client.aclose = AsyncMock()
            
            # Configure environmental integrator
            env_instance = mock_env.return_value
            env_instance.analyze_environmental_impacts = AsyncMock(return_value={
                "environmental_results": {
                    "gwp": 125.0,
                    "hct": 0.5,
                    "frs": 2.5,
                    "water_consumption": 200.0,
                    "allocated_impacts": {}
                }
            })
            env_instance.client = AsyncMock()
            env_instance.client.post = AsyncMock()
            env_instance.client.post.return_value.status_code = 200
            env_instance.client.post.return_value.json = AsyncMock(return_value={
                "environmental_results": {
                    "gwp": 125.0,
                    "hct": 0.5,
                    "frs": 2.5,
                    "water_consumption": 200.0
                }
            })
            env_instance.client.aclose = AsyncMock()
            
            yield {
                'technical': tech_instance,
                'economic': econ_instance,
                'environmental': env_instance
            }
    
    @pytest.fixture
    def valid_process_data(self):
        """Valid process data for testing"""
        equipment_cost = 50000.0
        initial_investment = -(equipment_cost * 1.35)  # Equipment + installation + indirect
        annual_revenue = 100000.0
        annual_opex = 57150.0  # From logs
        annual_cash_flow = annual_revenue - annual_opex
        
        # Define energy consumption values to maintain consistency
        electricity = 150.0
        cooling = 50.0
        
        return {
            "process_type": "baseline",
            "input_mass": 100.0,
            "output_mass": 80.0,
            "initial_protein_content": 25.0,
            "final_protein_content": 28.0,
            "initial_moisture_content": 15.0,
            "final_moisture_content": 10.0,
            "d10_particle_size": 10.0,
            "d50_particle_size": 50.0,
            "d90_particle_size": 90.0,
            "equipment_cost": equipment_cost,
            "maintenance_cost": 5000.0,
            "raw_material_cost": 2.5,
            "utility_cost": 1.5,
            "labor_cost": 25.0,
            "project_duration": 10,
            "discount_rate": 0.1,
            "production_volume": 1000.0,
            
            # Top-level fields for economic analysis
            "electricity_consumption": electricity,
            "cooling_consumption": cooling,
            
            # Nested structure for environmental analysis
            "energy_consumption": {
                "electricity": electricity,
                "cooling": cooling
            },
            "water_consumption": 200.0,
            "transport_consumption": 100.0,
            "equipment_mass": 1000.0,
            "thermal_ratio": 0.3,
            "production_data": {
                "input_mass": 100.0,
                "output_mass": 80.0,
                "production_volume": 1000.0
            },
            "product_values": {
                "main_product": annual_revenue,
                "waste_product": 0.0
            },
            "allocation_method": "hybrid",
            "hybrid_weights": {
                "physical": 0.5,
                "economic": 0.5
            },
            "air_flow": 500.0,
            "classifier_speed": 1500.0,
            "indirect_factors": [
                {
                    "name": "engineering",
                    "cost": equipment_cost,
                    "percentage": 0.15
                },
                {
                    "name": "contingency",
                    "cost": equipment_cost,
                    "percentage": 0.10
                },
                {
                    "name": "construction",
                    "cost": equipment_cost,
                    "percentage": 0.20
                }
            ],
            "installation_factor": 0.2,
            "indirect_costs_factor": 0.15,
            "maintenance_factor": 0.05,
            "cash_flows": [initial_investment] + [annual_cash_flow] * 10,
            "revenue_per_year": annual_revenue,
            "sensitivity_range": 0.2,
            "steps": 10,
            "equipment": [{
                "name": "main_equipment",
                "cost": equipment_cost,
                "efficiency": 0.85,
                "maintenance_cost": 5000.0,
                "energy_consumption": 150.0,
                "processing_capacity": 1000.0
            }],
            "utilities": [{
                "name": "electricity",
                "consumption": 150.0,
                "unit_price": 1.5,
                "unit": "kWh"
            }, {
                "name": "cooling",
                "consumption": 50.0,
                "unit_price": 1.5,
                "unit": "kWh"
            }, {
                "name": "water",
                "consumption": 200.0,
                "unit_price": 1.5,
                "unit": "kg"
            }],
            "raw_materials": [{
                "name": "feed_material",
                "quantity": 1000.0,
                "unit_price": 2.5,
                "unit": "kg"
            }],
            "labor_config": {
                "hourly_wage": 25.0,
                "hours_per_week": 40.0,
                "weeks_per_year": 52.0,
                "num_workers": 1
            }
        }
    
    @pytest.mark.asyncio
    async def test_service_initialization(self, service):
        """Test service initialization with integrators"""
        assert service.technical_integrator is not None
        assert service.economic_integrator is not None
        assert service.environmental_integrator is not None

    @pytest.mark.asyncio
    async def test_analyze_process(self, service, valid_process_data, mock_integrators, mock_httpx_client):
        """Test complete process analysis workflow"""
        # Configure mock HTTP client response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "efficiency_metrics": {
                "economic_indicators": {"npv_efficiency": 0.8},
                "quality_indicators": {"protein_efficiency": 0.9},
                "efficiency_metrics": {"resource_efficiency": 0.85}
            },
            "performance_indicators": {
                "eco_efficiency_index": 0.85,
                "relative_performance": 1.2
            }
        }
        mock_httpx_client.post.return_value = mock_response
        
        # Configure service client
        service.client = mock_httpx_client

        # Configure technical integrator responses
        mock_integrators['technical'].analyze_technical.return_value = {
            "technical_results": {
                "protein_recovery": 0.8,
                "separation_efficiency": 0.85,
                "process_efficiency": 0.75,
                "particle_size_distribution": {"d10": 10.0, "d50": 50.0, "d90": 90.0}
            }
        }

        # Configure economic integrator responses
        mock_integrators['economic'].analyze_economics.return_value = {
            'capex_analysis': {
                'summary': {
                    "equipment_costs": 50000.0,
                    "installation_costs": 10000.0,
                    "indirect_costs": 7500.0,
                    "total_capex": 67500.0
                },
                'equipment_breakdown': [{
                    "name": "main_equipment",
                    "cost": 50000.0,
                    "installation_cost": 10000.0,
                    "indirect_cost": 7500.0
                }],
                'process_type': "baseline"
            },
            'opex_analysis': {
                'summary': {
                    "utilities_cost": 5000.0,
                    "materials_cost": 3000.0,
                    "labor_cost": 5000.0,
                    "maintenance_cost": 2000.0,
                    "total_opex": 15000.0
                }
            },
            'profitability_analysis': {
                "metrics": {
                    "npv": 250000.0,
                    "roi": 0.25,
                    "payback_period": 3.5,
                    "profitability_index": 1.8
                }
            }
        }

        # Configure environmental integrator responses
        mock_integrators['environmental'].analyze_environmental_impacts.return_value = {
            'environmental_results': {
                'gwp': 100.0,
                'hct': 0.5,
                'frs': 200.0,
                'water_consumption': 150.0
            }
        }

        # Configure service integrators
        service.technical_integrator = mock_integrators['technical']
        service.economic_integrator = mock_integrators['economic']
        service.environmental_integrator = mock_integrators['environmental']

        # Execute analysis
        results = await service.analyze_process(valid_process_data)

        # Verify core result structure
        assert all(key in results for key in [
            'technical_results',
            'economic_analysis',
            'environmental_results',
            'efficiency_results'
        ])

        # Verify technical results
        assert 'protein_recovery' in results['technical_results']
        assert 'separation_efficiency' in results['technical_results']

        # Verify economic analysis
        assert 'capex_analysis' in results['economic_analysis']
        assert 'opex_analysis' in results['economic_analysis']
        assert 'profitability_analysis' in results['economic_analysis']

        # Verify environmental analysis
        assert 'environmental_results' in results['environmental_results']

        # Verify efficiency results
        assert 'efficiency_metrics' in results['efficiency_results']
        assert 'performance_indicators' in results['efficiency_results']

        # Verify HTTP client was called correctly
        mock_httpx_client.post.assert_called_once()
        assert "eco-efficiency/calculate" in mock_httpx_client.post.call_args[0][0]

    @pytest.mark.asyncio
    async def test_economic_analysis_integration(self, service, mock_integrators, valid_process_data):
        """Test economic analysis data preparation and integration"""
        # Configure economic integrator responses
        mock_capex_response = {
            "capex_summary": {
                "equipment_costs": 50000.0,
                "installation_costs": 10000.0,
                "indirect_costs": 7500.0,
                "total_capex": 67500.0
            },
            "equipment_breakdown": [{
                "name": "main_equipment",
                "cost": 50000.0,
                "installation_cost": 10000.0,
                "indirect_cost": 7500.0
            }],
            "process_type": "baseline"
        }

        mock_opex_response = {
            "opex_summary": {
                "utilities_cost": 5000.0,
                "materials_cost": 3000.0,
                "labor_cost": 5000.0,
                "maintenance_cost": 2000.0,
                "total_opex": 15000.0
            }
        }

        mock_profitability_response = {
            "metrics": {
                "npv": 250000.0,
                "roi": 0.25,
                "payback_period": 3.5,
                "profitability_index": 1.8
            }
        }

        # Configure economic integrator
        mock_integrators['economic'].analyze_economics.return_value = {
            'capex_analysis': mock_capex_response,
            'opex_analysis': mock_opex_response,
            'profitability_analysis': mock_profitability_response
        }

        # Configure service integrator
        service.economic_integrator = mock_integrators['economic']

        # Call analyze_economics directly
        economic_data = service._prepare_economic_data(valid_process_data)
        economic = await service.economic_integrator.analyze_economics(economic_data)

        # Verify core economic analysis structure
        assert all(key in economic for key in [
            'capex_analysis',
            'opex_analysis',
            'profitability_analysis'
        ])

        # Verify CAPEX structure
        capex = economic['capex_analysis']
        assert 'capex_summary' in capex
        assert 'equipment_breakdown' in capex

        # Verify OPEX structure
        opex = economic['opex_analysis']
        assert 'opex_summary' in opex

        # Verify profitability structure
        profitability = economic['profitability_analysis']
        assert 'metrics' in profitability

        # Verify the mock was called correctly
        mock_integrators['economic'].analyze_economics.assert_called_once_with(economic_data)

    @pytest.mark.asyncio
    async def test_environmental_analysis(self, service, valid_process_data):
        """Test environmental analysis data preparation"""
        results = service._prepare_environmental_data(valid_process_data)
            
        assert all(key in results for key in [
            "energy_consumption",
            "water_consumption",
            "process_type",
            "production_data"
        ])

    @pytest.mark.asyncio
    async def test_efficiency_analysis(self, service, mock_httpx_client):
        """Test efficiency analysis integration"""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "efficiency_metrics": {"eco_efficiency_index": 0.85},
            "performance_indicators": {"relative_performance": 1.2}
        }
        mock_httpx_client.post.return_value = mock_response

        data = {
            "economic_data": {},
            "quality_metrics": {},
            "environmental_impacts": {},
            "resource_inputs": {},
            "process_type": "baseline"
        }
        
        # Configure service client
        service.client = mock_httpx_client
        
        results = await service._analyze_efficiency(data)
        
        assert "efficiency_metrics" in results
        assert "performance_indicators" in results
        
        # Verify the mock was called correctly
        mock_httpx_client.post.assert_called_once()
        call_args = mock_httpx_client.post.call_args
        assert "eco-efficiency/calculate" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_error_handling(self, service, valid_process_data):
        """Test error handling in service integration"""
        # Test 1: RuntimeError from technical integrator
        error_message = "Analysis failed"
        
        # Configure technical integrator to raise error
        mock_technical = AsyncMock()
        mock_technical.analyze_technical.side_effect = RuntimeError(error_message)
        service.technical_integrator = mock_technical
        
        # Expect RuntimeError to be raised with the original error message
        with pytest.raises(RuntimeError) as exc_info:
            await service.analyze_process(valid_process_data)
        
        # Verify the error message and mock call
        assert error_message in str(exc_info.value)
        mock_technical.analyze_technical.assert_called_once()
        
        # Test 2: Connection error with retries
        # Reset technical integrator
        mock_technical.analyze_technical.reset_mock()
        mock_technical.analyze_technical.side_effect = None
        mock_technical.analyze_technical.return_value = {"technical_results": {}}
        
        # Configure economic integrator
        mock_economic = AsyncMock()
        mock_economic.analyze_economics.return_value = {
            "capex_analysis": {},
            "opex_analysis": {},
            "profitability_analysis": {}
        }
        service.economic_integrator = mock_economic
        
        # Configure environmental integrator
        mock_environmental = AsyncMock()
        mock_environmental.analyze_environmental_impacts.return_value = {
            "environmental_results": {}
        }
        service.environmental_integrator = mock_environmental
        
        # Configure HTTP client to simulate connection error
        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.ConnectError("Connection failed")
        service.client = mock_client
        
        # Test that connection errors trigger retries and eventually raise RetryError
        with pytest.raises(tenacity.RetryError):
            await service.analyze_process(valid_process_data)
        
        # Verify that the client attempted to make the request multiple times
        assert mock_client.post.call_count >= settings.FASTAPI_RETRY_COUNT

    @pytest.mark.asyncio
    async def test_multi_stage_process(self, service, valid_process_data):
        """Test multi-stage process data preparation"""
        # Add basic two-stage process data
        valid_process_data["process_stages"] = [
            {
                "feed": {"protein": 20, "moisture": 15},
                "product": {"protein": 25, "moisture": 12},
                "mass_flow": {"input": 1000, "output": 800}
            },
            {
                "feed": {"protein": 25, "moisture": 12},
                "product": {"protein": 30, "moisture": 10},
                "mass_flow": {"input": 800, "output": 600}
            }
        ]

        results = service._prepare_technical_data(valid_process_data)
        
        assert "separation_data" in results
        assert "process_data" in results["separation_data"]
        assert len(results["separation_data"]["process_data"]) == 2 