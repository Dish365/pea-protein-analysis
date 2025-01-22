import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from unittest.mock import AsyncMock, patch, MagicMock
from process_data.models.process import ProcessAnalysis, AnalysisResult
from process_data.services.fastapi_service import FastAPIService
import json
import asyncio
from asgiref.sync import sync_to_async
from django.core.cache import cache

pytestmark = [pytest.mark.django_db(transaction=True)]

@pytest.mark.django_db(transaction=True)
class TestProcessAnalysisPipeline:
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return APIClient()

    @pytest.fixture
    def mock_fastapi_service(self):
        """Mock FastAPI service"""
        with patch('process_data.services.fastapi_service.FastAPIService', autospec=True) as mock_service:
            service_instance = mock_service.return_value
            service_instance.__aenter__ = AsyncMock(return_value=service_instance)
            service_instance.__aexit__ = AsyncMock(return_value=None)
            service_instance.analyze_process = AsyncMock()
            service_instance.analyze_process.return_value = {
                "technical_results": {
                    "protein_recovery": {
                        "mass": 36.0,
                        "content": 45.0,
                        "yield": 0.8
                    },
                    "separation_efficiency": 0.85,
                    "process_efficiency": 0,
                    "particle_size_distribution": {
                        "d10": 10.0,
                        "d50": 50.0,
                        "d90": 90.0
                    }
                },
                "economic_analysis": {
                    "capex_analysis": {
                        "total_capex": 75000.0,
                        "equipment_cost": 50000.0,
                        "installation_cost": 15000.0,
                        "indirect_cost": 10000.0
                    },
                    "opex_analysis": {
                        "total_opex": 15000.0,
                        "utilities_cost": 5000.0,
                        "materials_cost": 5000.0,
                        "labor_cost": 3000.0,
                        "maintenance_cost": 2000.0
                    },
                    "profitability_analysis": {
                        "npv": 250000.0,
                        "roi": 0.25
                    }
                },
                "environmental_results": {
                    "impact_assessment": {
                        "gwp": 125.0,
                        "hct": 0.5,
                        "frs": 2.5
                    },
                    "consumption_metrics": {
                        "electricity": None,
                        "cooling": None,
                        "water": None
                    }
                },
                "efficiency_results": {
                    "efficiency_metrics": {
                        "eco_efficiency_index": 0.85
                    },
                    "performance_indicators": {
                        "relative_performance": 1.2
                    }
                }
            }
            service_instance.client = AsyncMock()
            service_instance.client.post = AsyncMock()
            service_instance.client.post.return_value.status_code = 200
            service_instance.client.post.return_value.json = AsyncMock(return_value=service_instance.analyze_process.return_value)
            service_instance.client.aclose = AsyncMock()
            yield service_instance

    @pytest.fixture
    def valid_process_data(self):
        """Valid process analysis input data"""
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

    @pytest.fixture
    def url(self):
        """Base URL for process analysis endpoints"""
        return reverse('v1:process_data:process-list-create')

    def test_process_analysis_creation(self, client, valid_process_data, mock_fastapi_service, url):
        """Test creating a new process analysis"""
        # Configure mock service
        mock_fastapi_service.analyze_process.return_value = mock_fastapi_service.analyze_process.return_value
        
        # Send request
        response = client.post(url, data=valid_process_data, format='json')
        
        # Verify response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert 'process_id' in data
        assert 'status' in data
        assert data['status'] == 'success'
        
        # Verify database record
        process = ProcessAnalysis.objects.get(id=data['process_id'])
        assert process.process_type == valid_process_data['process_type']
        assert process.input_mass == valid_process_data['input_mass']
        
        # Verify cache
        cache_key = f"process_analysis_{data['process_id']}"
        cache_data = cache.get(cache_key)
        assert cache_data is not None
        assert cache_data['status'] == 'completed'

    def test_invalid_input_data(self, client, valid_process_data, url):
        """Test validation of input data"""
        # Test with missing required field
        invalid_data = valid_process_data.copy()
        del invalid_data['input_mass']
        
        response = client.post(url, data=invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'input_mass' in response.json()['details']

    def test_process_analysis_retrieval(self, client, valid_process_data, mock_fastapi_service, url):
        """Test retrieving a specific process analysis"""
        # Create test process
        create_response = client.post(url, data=valid_process_data, format='json')
        process_id = create_response.json()['process_id']
        
        # Retrieve the analysis
        detail_url = reverse('v1:process_data:process-detail', args=[process_id])
        response = client.get(detail_url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == process_id
        assert data['process_type'] == valid_process_data['process_type']

    @pytest.mark.parametrize('field,invalid_value,expected_error', [
        ('input_mass', -1, 'min_value'),
        ('final_protein_content', 101, 'max_value'),
        ('discount_rate', -0.1, 'min_value'),
        ('process_type', 'invalid', 'choice'),
    ])
    def test_field_validation(self, client, valid_process_data, field, invalid_value, expected_error, url):
        """Test validation of specific fields"""
        data = valid_process_data.copy()
        data[field] = invalid_value
        
        response = client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field in response.json()['details']

    @pytest.mark.parametrize('process_type,extra_data', [
        ('baseline', {}),
        ('rf', {'electricity_consumption': 200.0}),
        ('ir', {'cooling_consumption': 100.0})
    ])
    def test_process_type_specific_analysis(self, client, valid_process_data, mock_fastapi_service, process_type, extra_data, url):
        """Test analysis for specific process types"""
        # Prepare data
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(extra_data)

        # Create a deep copy of the mock response
        mock_response = {
            "technical_results": mock_fastapi_service.analyze_process.return_value["technical_results"],
            "economic_analysis": mock_fastapi_service.analyze_process.return_value["economic_analysis"],
            "environmental_results": {
                "impact_assessment": {
                    "gwp": 125.0,
                    "hct": 0.5,
                    "frs": 2.5
                },
                "consumption_metrics": {
                    "electricity": data.get("electricity_consumption") if process_type == 'rf' else None,
                    "cooling": data.get("cooling_consumption") if process_type == 'ir' else None,
                    "water": None
                }
            },
            "efficiency_results": mock_fastapi_service.analyze_process.return_value["efficiency_results"],
            "process_type": process_type,
            "electricity_consumption": data.get("electricity_consumption"),
            "cooling_consumption": data.get("cooling_consumption")
        }

        # Configure mock
        mock_fastapi_service.analyze_process = AsyncMock(return_value=mock_response)

        response = client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # Verify process type specific handling
        result_data = response.json()
        assert 'summary' in result_data
        if process_type == 'rf':
            assert 'environmental' in result_data['summary']
            assert 'consumption_metrics' in result_data['summary']['environmental']
            assert 'electricity' in result_data['summary']['environmental']['consumption_metrics']
            assert result_data['summary']['environmental']['consumption_metrics']['electricity'] == data['electricity_consumption']
        elif process_type == 'ir':
            assert 'environmental' in result_data['summary']
            assert 'consumption_metrics' in result_data['summary']['environmental']
            assert 'cooling' in result_data['summary']['environmental']['consumption_metrics']
            assert result_data['summary']['environmental']['consumption_metrics']['cooling'] == data['cooling_consumption']

    def test_analysis_progress_tracking(self, client, valid_process_data, mock_fastapi_service, url):
        """Test analysis progress tracking"""
        # Start analysis
        response = client.post(url, data=valid_process_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        process_id = response.json()['process_id']
        
        # Check progress
        status_url = reverse('v1:process_data:process-status', args=[process_id])
        response = client.get(status_url)
        assert response.status_code == status.HTTP_200_OK
        
        status_data = response.json()
        assert 'status' in status_data
        assert 'progress' in status_data
        assert status_data['status'] in ['processing', 'completed']

    def test_process_analysis_list(self, client, valid_process_data, url):
        """Test listing all process analyses"""
        # Create a few process analyses
        for _ in range(3):
            client.post(url, data=valid_process_data, format='json')

        # List all analyses
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_progress_tracking(self, client, valid_process_data, mock_fastapi_service, url):
        """Test tracking analysis progress"""
        # Create a process analysis
        create_response = client.post(url, data=valid_process_data, format='json')
        process_id = create_response.json()['process_id']

        # Check progress
        status_url = reverse('v1:process_data:process-status', args=[process_id])
        response = client.get(status_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'progress' in data
    
    @pytest.mark.parametrize('process_type,valid_data_updates', [
        ('baseline', {}),
        ('rf', {'electricity_consumption': 200.0}),
        ('ir', {'cooling_consumption': 100.0})
    ])
    def test_process_type_comparison(self, client, valid_process_data, mock_fastapi_service, process_type, valid_data_updates, url):
        """Test comparison between different process types"""
        # Update data for specific process type
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(valid_data_updates)

        response = client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
    
    @pytest.mark.parametrize('process_type,invalid_data', [
        ('rf', {'electricity_consumption': 0}),  # RF requires positive electricity
        ('ir', {'cooling_consumption': 0}),  # IR requires positive cooling
        ('baseline', {'process_type': 'invalid'}),  # Invalid process type
    ])
    def test_process_type_validation(self, client, valid_process_data, process_type, invalid_data, url):
        """Test validation for process type specific requirements"""
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(invalid_data)

        response = client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST 