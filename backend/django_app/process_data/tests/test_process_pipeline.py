import pytest
from django.test import AsyncClient
from django.urls import reverse
from rest_framework import status
from unittest.mock import AsyncMock, patch, MagicMock
from process_data.models.process import ProcessAnalysis, AnalysisResult
from process_data.services.fastapi_service import FastAPIService
import json
import asyncio
from rest_framework.test import APIRequestFactory
from asgiref.sync import sync_to_async
from django.core.cache import cache

pytestmark = [pytest.mark.asyncio, pytest.mark.django_db(transaction=True)]

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestProcessAnalysisPipeline:
    @pytest.fixture
    def valid_process_data(self):
        """Valid process analysis input data"""
        return {
            "process_type": "baseline",
            "input_mass": 100.0,
            "output_mass": 80.0,
            "initial_protein_content": 25.0,
            "final_protein_content": 45.0,
            "initial_moisture_content": 15.0,
            "final_moisture_content": 10.0,
            "d10_particle_size": 10.0,
            "d50_particle_size": 50.0,
            "d90_particle_size": 90.0,
            "equipment_cost": 50000.0,
            "maintenance_cost": 5000.0,
            "raw_material_cost": 2.5,
            "utility_cost": 1.5,
            "labor_cost": 25.0,
            "project_duration": 10,
            "discount_rate": 0.1,
            "production_volume": 1000.0,
            "electricity_consumption": 150.0,
            "cooling_consumption": 50.0,
            "water_consumption": 200.0
        }
    
    @pytest.fixture
    def mock_analysis_results(self):
        """Mock analysis results from FastAPI service"""
        return {
            "technical_results": {
                "protein_recovery": {
                    "mass": 36.0,
                    "content": 45.0,
                    "yield": 0.8
                },
                "separation_efficiency": 0.85,
                "particle_analysis": {
                    "d10": 10.0,
                    "d50": 50.0,
                    "d90": 90.0
                }
            },
            "economic_results": {
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
                    "frs": 2.5,
                    "water_consumption": 200.0
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
    
    @pytest.fixture
    async def mock_fastapi_service(self, mock_analysis_results):
        """Mock FastAPI service"""
        with patch('process_data.services.fastapi_service.FastAPIService', autospec=True) as mock_service:
            service_instance = mock_service.return_value
            service_instance.__aenter__ = AsyncMock(return_value=service_instance)
            service_instance.__aexit__ = AsyncMock(return_value=None)
            service_instance.analyze_process = AsyncMock(return_value=mock_analysis_results)
            yield service_instance
    
    @pytest.fixture
    def url(self):
        """Base URL for process analysis endpoints"""
        return reverse('v1:process_data:process-list-create')

    @pytest.fixture
    async def async_client(self):
        return AsyncClient()

    async def test_process_analysis_creation(self, async_client, valid_process_data, mock_fastapi_service, url, mock_analysis_results):
        """Test creating a new process analysis"""
        # Configure mock service
        mock_fastapi_service.analyze_process.return_value = mock_analysis_results
        
        # Send request
        response = await async_client.post(url, data=json.dumps(valid_process_data), content_type='application/json')
        
        # Verify response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert 'process_id' in data
        assert 'status' in data
        assert data['status'] == 'success'
        
        # Verify database record
        process = await ProcessAnalysis.objects.aget(id=data['process_id'])
        assert process.process_type == valid_process_data['process_type']
        assert process.input_mass == valid_process_data['input_mass']
        
        # Verify cache
        cache_key = f"process_analysis_{data['process_id']}"
        cache_data = cache.get(cache_key)
        assert cache_data is not None
        assert cache_data['status'] == 'completed'

    async def test_invalid_input_data(self, async_client, valid_process_data, url):
        """Test validation of input data"""
        # Test with missing required field
        invalid_data = valid_process_data.copy()
        del invalid_data['input_mass']
        
        response = await async_client.post(url, data=json.dumps(invalid_data), content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'input_mass' in response.json()

    async def test_fastapi_service_error(self, async_client, valid_process_data, mock_fastapi_service, url):
        """Test handling of FastAPI service errors"""
        # Configure mock to raise exception
        mock_fastapi_service.analyze_process.side_effect = Exception("Service error")
        
        response = await async_client.post(url, data=json.dumps(valid_process_data), content_type='application/json')
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert 'error' in response.json()

    async def test_process_analysis_retrieval(self, async_client, valid_process_data, mock_fastapi_service, url, mock_analysis_results, create_test_process, create_test_result):
        """Test retrieving a specific process analysis"""
        # Create test process and result
        process = await create_test_process(valid_process_data)
        await create_test_result(process, mock_analysis_results)
        
        # Retrieve the analysis
        detail_url = reverse('v1:process_data:process-detail', args=[process.id])
        response = await async_client.get(detail_url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == process.id
        assert data['process_type'] == valid_process_data['process_type']

    @pytest.mark.parametrize('field,invalid_value,expected_error', [
        ('input_mass', -1, 'min_value'),
        ('final_protein_content', 101, 'max_value'),
        ('discount_rate', -0.1, 'min_value'),
        ('process_type', 'invalid', 'choice'),
    ])
    async def test_field_validation(self, async_client, valid_process_data, field, invalid_value, expected_error, url):
        """Test validation of specific fields"""
        data = valid_process_data.copy()
        data[field] = invalid_value
        
        response = await async_client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field in response.json()

    @pytest.mark.parametrize('process_type,extra_data', [
        ('baseline', {}),
        ('rf', {'electricity_consumption': 200.0}),
        ('ir', {'cooling_consumption': 100.0})
    ])
    async def test_process_type_specific_analysis(self, async_client, valid_process_data, mock_fastapi_service, process_type, extra_data, url, mock_analysis_results):
        """Test analysis for specific process types"""
        # Configure mock
        mock_fastapi_service.analyze_process.return_value = mock_analysis_results
        
        # Prepare data
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(extra_data)
        
        response = await async_client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify process type specific handling
        result_data = response.json()
        if process_type == 'rf':
            assert 'electricity_consumption' in result_data['summary']['technical']
        elif process_type == 'ir':
            assert 'cooling_consumption' in result_data['summary']['technical']

    async def test_analysis_progress_tracking(self, async_client, valid_process_data, mock_fastapi_service, url, mock_analysis_results):
        """Test analysis progress tracking"""
        # Configure mock with delay to simulate processing
        async def delayed_analysis(*args, **kwargs):
            await asyncio.sleep(0.1)
            return mock_analysis_results
        
        mock_fastapi_service.analyze_process.side_effect = delayed_analysis
        
        # Start analysis
        response = await async_client.post(url, data=json.dumps(valid_process_data), content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        process_id = response.json()['process_id']
        
        # Check progress
        status_url = reverse('v1:process_data:process-status', args=[process_id])
        response = await async_client.get(status_url)
        assert response.status_code == status.HTTP_200_OK
        
        status_data = response.json()
        assert 'status' in status_data
        assert 'progress' in status_data
        assert status_data['status'] in ['processing', 'completed']

    async def test_process_analysis_list(self, async_client, valid_process_data, mock_fastapi_service, url):
        """Test listing all process analyses"""
        # Create a few process analyses
        for _ in range(3):
            await async_client.post(url, data=valid_process_data, content_type='application/json')

        # List all analyses
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    async def test_progress_tracking(self, async_client, valid_process_data, mock_fastapi_service, url):
        """Test tracking analysis progress"""
        # Create a process analysis
        create_response = await async_client.post(url, data=valid_process_data, content_type='application/json')
        process_id = create_response.json()['process_id']

        # Check progress
        status_url = reverse('v1:process_data:process-status', args=[process_id])
        response = await async_client.get(status_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'progress' in data
    
    @pytest.mark.parametrize('process_type,valid_data_updates', [
        ('baseline', {}),
        ('rf', {'electricity_consumption': 200.0}),
        ('ir', {'cooling_consumption': 100.0})
    ])
    async def test_process_type_comparison(self, async_client, valid_process_data, mock_fastapi_service, process_type, valid_data_updates, url):
        """Test comparison between different process types"""
        # Update data for specific process type
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(valid_data_updates)

        response = await async_client.post(url, data=data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
    
    @pytest.mark.parametrize('process_type,invalid_data', [
        ('rf', {'electricity_consumption': 0}),  # RF requires positive electricity
        ('ir', {'cooling_consumption': 0}),  # IR requires positive cooling
        ('baseline', {'process_type': 'invalid'}),  # Invalid process type
    ])
    async def test_process_type_validation(self, async_client, valid_process_data, process_type, invalid_data, url):
        """Test validation for process type specific requirements"""
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(invalid_data)

        response = await async_client.post(url, data=data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    async def test_process_type_comparison(self, async_client, valid_process_data, mock_fastapi_service, url):
        """Test comparison between different process types"""
        process_types = ['baseline', 'rf', 'ir']
        results = {}

        for process_type in process_types:
            data = valid_process_data.copy()
            data['process_type'] = process_type

            # Add process-specific requirements
            if process_type == 'rf':
                data['electricity_consumption'] = 200.0
            elif process_type == 'ir':
                data['cooling_consumption'] = 100.0

            response = await async_client.post(url, data=data, content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED
            results[process_type] = response.json()

        # Verify each process type has unique characteristics
        assert results['rf']['summary']['technical']['electricity_consumption'] > results['baseline']['summary']['technical']['electricity_consumption']
        assert results['ir']['summary']['technical']['cooling_consumption'] > results['baseline']['summary']['technical']['cooling_consumption'] 