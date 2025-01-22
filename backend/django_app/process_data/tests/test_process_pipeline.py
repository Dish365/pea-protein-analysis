import pytest
from django.urls import reverse
from rest_framework import status
import logging
from asgiref.sync import sync_to_async
from process_data.models.process import ProcessAnalysis, AnalysisResult
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

logger = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.asyncio
]

class TestProcessAnalysisPipeline:
    @pytest.fixture
    def url(self):
        """Base URL for process analysis endpoints"""
        return reverse('v1:process_data:process-list-create')
    
    async def test_process_analysis_creation(self, client, mock_process_input, mock_fastapi_service, url):
        """Test creating a new process analysis"""
        response = client.post(url, data=mock_process_input, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert 'process_id' in data
        assert 'status' in data
        assert data['status'] == 'success'
        
        process = await sync_to_async(ProcessAnalysis.objects.get)(id=data['process_id'])
        assert process.process_type == mock_process_input['process_type']

    async def test_real_api_integration(self, client, mock_process_input, real_fastapi_service, url):
        """Test integration with real FastAPI endpoints"""
        try:
            # Send analysis request to real endpoints
            results = await real_fastapi_service.analyze_process(mock_process_input)
            logger.debug(f"Received results from FastAPI: {results}")
            
            # Verify response structure and data
            await self._verify_results_structure(results)
            
            # Create process analysis using real results
            response = client.post(url, data=mock_process_input, format='json')
            assert response.status_code == status.HTTP_201_CREATED
            
            process_id = response.json()['process_id']
            process = await sync_to_async(ProcessAnalysis.objects.get)(id=process_id)
            result = await sync_to_async(AnalysisResult.objects.get)(process_id=process.id)
            
            # Verify result storage
            await self._verify_stored_results(result)
            
        except Exception as e:
            logger.error(f"Error in real API test: {str(e)}", exc_info=True)
            raise

    async def _verify_results_structure(self, results):
        """Verify the structure of analysis results"""
        # Technical Results
        assert "technical_results" in results
        tech = results["technical_results"]
        assert "protein_recovery" in tech
        assert "separation_efficiency" in tech
        assert "process_efficiency" in tech
        assert "particle_size_distribution" in tech
        
        # Economic Results
        assert "economic_analysis" in results
        econ = results["economic_analysis"]
        assert "capex_analysis" in econ
        assert "opex_analysis" in econ
        assert "profitability_analysis" in econ
        
        # Environmental Results
        assert "environmental_results" in results
        env = results["environmental_results"]
        assert "impact_assessment" in env
        assert "consumption_metrics" in env
        
        # Efficiency Results
        assert "efficiency_results" in results
        eff = results["efficiency_results"]
        assert "efficiency_metrics" in eff
        assert "performance_indicators" in eff

    async def _verify_stored_results(self, result):
        """Verify stored analysis results"""
        assert result.technical_results is not None
        assert result.economic_results is not None
        assert result.environmental_results is not None
        assert result.efficiency_results is not None
        
        # Verify specific values based on your application's requirements
        tech = result.technical_results
        assert "protein_recovery" in tech
        assert "separation_efficiency" in tech
        
        econ = result.economic_results
        assert "capex_analysis" in econ
        assert "opex_analysis" in econ
        
        env = result.environmental_results
        assert "impact_assessment" in env
        
        eff = result.efficiency_results
        assert "efficiency_metrics" in eff

    async def test_process_status_tracking(self, client, mock_process_input, mock_fastapi_service, url):
        """Test process status tracking"""
        # Create process
        response = client.post(url, data=mock_process_input, format='json')
        process_id = response.json()['process_id']
        
        # Check status
        status_url = reverse('v1:process_data:process-status', args=[process_id])
        status_response = client.get(status_url)
        
        assert status_response.status_code == status.HTTP_200_OK
        status_data = status_response.json()
        assert 'status' in status_data
        assert 'progress' in status_data
        assert status_data['status'] in ['processing', 'completed']

    @pytest.mark.parametrize('field,invalid_value', [
        ('process_type', 'invalid'),
        ('technical_params.initial_moisture', -1),
        ('economic_params.discount_rate', -0.1),
        ('environmental_params.electricity_consumption', -100)
    ])
    async def test_input_validation(self, client, mock_process_input, field, invalid_value, url):
        """Test input validation"""
        data = mock_process_input.copy()
        field_parts = field.split('.')
        
        # Set nested invalid value
        current = data
        for part in field_parts[:-1]:
            current = current[part]
        current[field_parts[-1]] = invalid_value
        
        response = client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST