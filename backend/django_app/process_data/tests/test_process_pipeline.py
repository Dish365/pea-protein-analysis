import pytest
from django.test import AsyncClient
from django.urls import reverse
from rest_framework import status
from unittest.mock import AsyncMock, patch, MagicMock
from ..models.process import ProcessAnalysis, AnalysisResult
from ..services.fastapi_service import FastAPIService
import json

@pytest.mark.django_db
@pytest.mark.asyncio
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
            "technical_analysis": {
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
                },
                "economic_analysis": {
                    "product_prices": {"protein": 5.0},
                    "production_volumes": {"protein": 1000.0}
                }
            },
            "environmental_analysis": {
                "impact_assessment": {
                    "gwp": 125.0,
                    "hct": 0.5,
                    "frs": 2.5,
                    "water_consumption": 200.0
                }
            },
            "eco_efficiency_analysis": {
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
    
    async def test_process_analysis_creation(self, client, valid_process_data, mock_fastapi_service):
        """Test successful creation of process analysis"""
        url = reverse('process-analysis')
        response = await client.post(url, data=valid_process_data, content_type='application/json')
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Verify response structure
        assert 'process_id' in data
        assert data['status'] == 'success'
        assert all(key in data for key in [
            'technical_analysis',
            'economic_analysis',
            'environmental_analysis',
            'eco_efficiency_analysis'
        ])
        
        # Verify database entries
        process = await ProcessAnalysis.objects.aget(id=data['process_id'])
        assert process.process_type == valid_process_data['process_type']
        
        result = await AnalysisResult.objects.aget(process=process)
        assert result.protein_yield == 0.8
        assert result.eco_efficiency_index == 0.85
    
    async def test_invalid_input_data(self, client):
        """Test process analysis with invalid input data"""
        url = reverse('process-analysis')
        invalid_data = {
            "process_type": "invalid_type",
            "input_mass": -100.0  # Invalid negative mass
        }
        
        response = await client.post(url, data=invalid_data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert 'process_type' in data  # Should contain validation error
        assert 'input_mass' in data  # Should contain validation error
    
    async def test_fastapi_service_error(self, client, valid_process_data, mock_fastapi_service):
        """Test handling of FastAPI service errors"""
        mock_fastapi_service.analyze_process.side_effect = RuntimeError("Service unavailable")
        
        url = reverse('process-analysis')
        response = await client.post(url, data=valid_process_data, content_type='application/json')
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert 'error' in data
        assert 'Service unavailable' in data['error']
        
        # Verify no process was created
        assert await ProcessAnalysis.objects.acount() == 0
    
    async def test_process_analysis_retrieval(self, client, valid_process_data, mock_fastapi_service):
        """Test retrieval of existing process analysis"""
        # First create a process
        url = reverse('process-analysis')
        response = await client.post(url, data=valid_process_data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        process_id = response.json()['process_id']
        
        # Then retrieve it
        url = reverse('process-analysis-detail', kwargs={'process_id': process_id})
        response = await client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['status'] == 'completed'
        assert 'process' in data
        assert 'results' in data
    
    async def test_process_analysis_list(self, client, valid_process_data, mock_fastapi_service):
        """Test listing all process analyses"""
        # Create multiple processes
        url = reverse('process-analysis')
        await client.post(url, data=valid_process_data, content_type='application/json')
        await client.post(url, data=valid_process_data, content_type='application/json')
        
        # Get list
        url = reverse('process-analysis-list')
        response = await client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2  # Should have 2 processes
    
    async def test_progress_tracking(self, client, valid_process_data, mock_fastapi_service):
        """Test process analysis progress tracking"""
        url = reverse('process-analysis')
        
        # Start analysis
        response = await client.post(url, data=valid_process_data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        process_id = response.json()['process_id']
        
        # Check progress immediately
        url = reverse('process-analysis-detail', kwargs={'process_id': process_id})
        response = await client.get(url)
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert data['status'] == 'completed'  # Since we're using mocks, it completes immediately
        
    @pytest.mark.parametrize('field,invalid_value', [
        ('input_mass', 0),  # Zero mass
        ('final_protein_content', 101),  # Over 100%
        ('discount_rate', -0.1),  # Negative rate
        ('d50_particle_size', 'invalid'),  # Non-numeric
    ])
    async def test_field_validation(self, client, valid_process_data, field, invalid_value):
        """Test validation of specific fields"""
        data = valid_process_data.copy()
        data[field] = invalid_value
        
        url = reverse('process-analysis')
        response = await client.post(url, data=data, content_type='application/json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field in response.json()  # Should contain validation error for the field 
    
    @pytest.mark.parametrize('process_type,valid_data_updates', [
        ('baseline', {}),
        ('rf', {'electricity_consumption': 200.0}),
        ('ir', {'cooling_consumption': 100.0})
    ])
    async def test_process_type_specific_analysis(self, client, valid_process_data, mock_fastapi_service, process_type, valid_data_updates):
        """Test analysis for specific process types"""
        # Update data for specific process type
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(valid_data_updates)
        
        url = reverse('process-analysis')
        response = await client.post(url, data=data, content_type='application/json')
        
        assert response.status_code == status.HTTP_201_CREATED
        result_data = response.json()
        
        # Verify process type specific results
        if process_type == 'rf':
            assert result_data['technical_analysis']['separation_efficiency'] > 0.8
            assert result_data['environmental_analysis']['impact_assessment']['electricity_consumption'] > 0
        elif process_type == 'ir':
            assert result_data['technical_analysis']['separation_efficiency'] > 0.75
            assert result_data['environmental_analysis']['impact_assessment']['cooling_consumption'] > 0
    
    @pytest.mark.parametrize('process_type,invalid_data', [
        ('rf', {'electricity_consumption': 0}),  # RF requires positive electricity
        ('ir', {'cooling_consumption': 0}),  # IR requires positive cooling
        ('baseline', {'process_type': 'invalid'}),  # Invalid process type
    ])
    async def test_process_type_validation(self, client, valid_process_data, process_type, invalid_data):
        """Test validation for process type specific requirements"""
        data = valid_process_data.copy()
        data['process_type'] = process_type
        data.update(invalid_data)
        
        url = reverse('process-analysis')
        response = await client.post(url, data=data, content_type='application/json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_data = response.json()
        
        if process_type == 'rf':
            assert 'electricity_consumption' in error_data
        elif process_type == 'ir':
            assert 'cooling_consumption' in error_data
        else:
            assert 'process_type' in error_data
    
    async def test_process_type_comparison(self, client, valid_process_data, mock_fastapi_service):
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
            
            url = reverse('process-analysis')
            response = await client.post(url, data=data, content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED
            results[process_type] = response.json()
        
        # Verify each process type has unique characteristics
        # Baseline should have balanced metrics
        assert results['baseline']['eco_efficiency_analysis']['efficiency_metrics']['eco_efficiency_index'] > 0
        
        # RF should have higher electricity impact but better separation
        assert results['rf']['technical_analysis']['separation_efficiency'] > \
               results['baseline']['technical_analysis']['separation_efficiency']
        assert results['rf']['environmental_analysis']['impact_assessment']['electricity_consumption'] > \
               results['baseline']['environmental_analysis']['impact_assessment']['electricity_consumption']
        
        # IR should have higher cooling impact but better protein recovery
        assert results['ir']['technical_analysis']['protein_recovery']['yield'] > \
               results['baseline']['technical_analysis']['protein_recovery']['yield']
        assert results['ir']['environmental_analysis']['impact_assessment']['cooling_consumption'] > \
               results['baseline']['environmental_analysis']['impact_assessment']['cooling_consumption'] 