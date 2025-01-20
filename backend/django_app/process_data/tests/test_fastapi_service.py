import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from django.conf import settings
from ..services.fastapi_service import FastAPIService
from tenacity import RetryError
from process_data.models import Process, AnalysisResults

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
                "protein_recovery": {"mass": 36.0, "content": 45.0, "yield": 0.8},
                "separation_efficiency": 0.85,
                "particle_analysis": {"d10": 10.0, "d50": 50.0, "d90": 90.0}
            })
            tech_instance.client = AsyncMock()
            tech_instance.client.aclose = AsyncMock()
            
            # Configure economic integrator
            econ_instance = mock_econ.return_value
            econ_instance.analyze_economics = AsyncMock(return_value={
                "capex_analysis": {"total_capex": 75000.0},
                "opex_analysis": {"total_opex": 15000.0},
                "profitability_analysis": {"npv": 250000.0, "roi": 0.25},
                "economic_analysis": {
                    "product_prices": {"protein": 5.0},
                    "production_volumes": {"protein": 1000.0}
                }
            })
            econ_instance.client = AsyncMock()
            econ_instance.client.aclose = AsyncMock()
            
            # Configure environmental integrator
            env_instance = mock_env.return_value
            env_instance.analyze_environmental_impacts = AsyncMock(return_value={
                "impact_assessment": {
                    "gwp": 125.0,
                    "hct": 0.5,
                    "frs": 2.5,
                    "water_consumption": 200.0
                }
            })
            env_instance.client = AsyncMock()
            env_instance.client.aclose = AsyncMock()
            
            yield {
                'technical': tech_instance,
                'economic': econ_instance,
                'environmental': env_instance
            }
    
    @pytest.fixture
    def valid_process_data(self):
        """Valid process data for testing"""
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
    
    async def test_successful_analysis(self, service, mock_httpx_client, mock_integrators, valid_process_data):
        """Test successful process analysis"""
        # Configure mock response for efficiency calculation
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "efficiency_metrics": {"eco_efficiency_index": 0.85},
            "performance_indicators": {"relative_performance": 1.2}
        }
        mock_httpx_client.post.return_value = mock_response
        
        async with service:
            results = await service.analyze_process(valid_process_data)
        
        # Verify results structure
        assert all(key in results for key in [
            'technical_analysis',
            'economic_analysis',
            'environmental_analysis',
            'eco_efficiency_analysis'
        ])
        
        # Verify integrator calls
        mock_integrators['technical'].analyze_technical.assert_called_once()
        mock_integrators['economic'].analyze_economics.assert_called_once()
        mock_integrators['environmental'].analyze_environmental_impacts.assert_called_once()
        
        # Verify efficiency calculation call
        mock_httpx_client.post.assert_called_once()
        assert mock_httpx_client.post.call_args[0][0].endswith('/efficiency/calculate')
    
    async def test_technical_analysis_failure(self, service, mock_httpx_client, mock_integrators, valid_process_data):
        """Test handling of technical analysis failure"""
        mock_integrators['technical'].analyze_technical.side_effect = RuntimeError("Technical analysis failed")
        
        with pytest.raises(RuntimeError, match="Technical analysis failed"):
            async with service:
                await service.analyze_process(valid_process_data)
    
    async def test_efficiency_calculation_failure(self, service, mock_httpx_client, mock_integrators, valid_process_data):
        """Test handling of efficiency calculation failure"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_response.raise_for_status.side_effect = httpx.HTTPError("Server error")
        mock_httpx_client.post.return_value = mock_response
        
        with pytest.raises(RuntimeError, match="Eco-efficiency analysis failed"):
            async with service:
                await service.analyze_process(valid_process_data)
    
    async def test_retry_mechanism(self, service, mock_httpx_client, mock_integrators, valid_process_data):
        """Test retry mechanism for transient failures"""
        # Configure mock to fail twice then succeed
        mock_response_fail = MagicMock()
        mock_response_fail.status_code = 500
        mock_response_fail.raise_for_status.side_effect = httpx.HTTPError("Temporary error")
        
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {
            "efficiency_metrics": {"eco_efficiency_index": 0.85},
            "performance_indicators": {"relative_performance": 1.2}
        }
        
        mock_httpx_client.post.side_effect = [
            mock_response_fail,
            mock_response_fail,
            mock_response_success
        ]
        
        async with service:
            results = await service.analyze_process(valid_process_data)
        
        assert mock_httpx_client.post.call_count == 3
        assert 'eco_efficiency_analysis' in results
    
    async def test_parallel_execution(self, service, mock_httpx_client, mock_integrators, valid_process_data):
        """Test parallel execution of analyses"""
        # Add delays to integrator calls to verify parallel execution
        async def delayed_technical(*args, **kwargs):
            await asyncio.sleep(0.1)
            return mock_integrators['technical'].analyze_technical.return_value
        
        async def delayed_economic(*args, **kwargs):
            await asyncio.sleep(0.1)
            return mock_integrators['economic'].analyze_economics.return_value
        
        async def delayed_environmental(*args, **kwargs):
            await asyncio.sleep(0.1)
            return mock_integrators['environmental'].analyze_environmental_impacts.return_value
        
        mock_integrators['technical'].analyze_technical = AsyncMock(side_effect=delayed_technical)
        mock_integrators['economic'].analyze_economics = AsyncMock(side_effect=delayed_economic)
        mock_integrators['environmental'].analyze_environmental_impacts = AsyncMock(side_effect=delayed_environmental)
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "efficiency_metrics": {"eco_efficiency_index": 0.85},
            "performance_indicators": {"relative_performance": 1.2}
        }
        mock_httpx_client.post.return_value = mock_response
        
        import time
        start_time = time.time()
        
        async with service:
            results = await service.analyze_process(valid_process_data)
        
        execution_time = time.time() - start_time
        
        # Verify that execution time is closer to 0.1s than 0.3s
        assert execution_time < 0.2  # Should be ~0.1s plus small overhead
        
        # Verify all analyses were called
        assert mock_integrators['technical'].analyze_technical.called
        assert mock_integrators['economic'].analyze_economics.called
        assert mock_integrators['environmental'].analyze_environmental_impacts.called

    @pytest.mark.asyncio
    async def test_service_initialization(self, service):
        """Test FastAPI service initialization"""
        assert service.technical_integrator is not None
        assert service.economic_integrator is not None
        assert service.environmental_integrator is not None

    @pytest.mark.asyncio
    async def test_analyze_process(self, service, mock_process_input, mock_fastapi_response):
        """Test complete process analysis through FastAPI"""
        # Create test process
        process = await Process.objects.acreate(
            technical_params=mock_process_input['technical_params'],
            economic_params=mock_process_input['economic_params'],
            environmental_params=mock_process_input['environmental_params']
        )

        # Mock integrator responses
        with patch.object(service.technical_integrator, 'analyze_technical', new_callable=AsyncMock) as mock_technical, \
             patch.object(service.economic_integrator, 'analyze_economics', new_callable=AsyncMock) as mock_economic, \
             patch.object(service.environmental_integrator, 'analyze_environmental', new_callable=AsyncMock) as mock_environmental:
            
            mock_technical.return_value = mock_fastapi_response['technical']
            mock_economic.return_value = mock_fastapi_response['economic']
            mock_environmental.return_value = mock_fastapi_response['environmental']

            # Execute analysis
            results = await service.analyze_process(process.id)

            # Verify results
            assert results['technical'] == mock_fastapi_response['technical']
            assert results['economic'] == mock_fastapi_response['economic']
            assert results['environmental'] == mock_fastapi_response['environmental']

    @pytest.mark.asyncio
    async def test_technical_analysis(self, service, mock_process_input, mock_fastapi_response):
        """Test technical analysis integration"""
        process = await Process.objects.acreate(technical_params=mock_process_input['technical_params'])

        with patch.object(service.technical_integrator, 'analyze_technical', new_callable=AsyncMock) as mock_technical:
            mock_technical.return_value = mock_fastapi_response['technical']
            
            results = await service._analyze_technical_metrics(process)
            
            assert results['protein_recovery'] == mock_fastapi_response['technical']['protein_recovery']
            assert results['moisture_content'] == mock_fastapi_response['technical']['moisture_content']
            mock_technical.assert_called_once()

    @pytest.mark.asyncio
    async def test_economic_analysis(self, service, mock_process_input, mock_fastapi_response):
        """Test economic analysis integration"""
        process = await Process.objects.acreate(economic_params=mock_process_input['economic_params'])

        with patch.object(service.economic_integrator, 'analyze_economics', new_callable=AsyncMock) as mock_economic:
            mock_economic.return_value = mock_fastapi_response['economic']
            
            results = await service._analyze_economics(process)
            
            assert results['capex'] == mock_fastapi_response['economic']['capex']
            assert results['opex'] == mock_fastapi_response['economic']['opex']
            assert results['profitability'] == mock_fastapi_response['economic']['profitability']
            mock_economic.assert_called_once()

    @pytest.mark.asyncio
    async def test_environmental_analysis(self, service, mock_process_input, mock_fastapi_response):
        """Test environmental analysis integration"""
        process = await Process.objects.acreate(environmental_params=mock_process_input['environmental_params'])

        with patch.object(service.environmental_integrator, 'analyze_environmental', new_callable=AsyncMock) as mock_environmental:
            mock_environmental.return_value = mock_fastapi_response['environmental']
            
            results = await service._analyze_environmental(process)
            
            assert results['direct_impacts'] == mock_fastapi_response['environmental']['direct_impacts']
            assert results['allocated_impacts'] == mock_fastapi_response['environmental']['allocated_impacts']
            mock_environmental.assert_called_once()

    @pytest.mark.asyncio
    async def test_efficiency_analysis(self, service, mock_fastapi_response):
        """Test efficiency analysis integration"""
        economic_results = mock_fastapi_response['economic']
        environmental_results = mock_fastapi_response['environmental']

        with patch.object(service, '_calculate_efficiency', new_callable=AsyncMock) as mock_efficiency:
            mock_efficiency.return_value = mock_fastapi_response['efficiency']
            
            results = await service._analyze_efficiency(economic_results, environmental_results)
            
            assert results['technical_score'] == mock_fastapi_response['efficiency']['technical_score']
            assert results['economic_score'] == mock_fastapi_response['efficiency']['economic_score']
            assert results['environmental_score'] == mock_fastapi_response['efficiency']['environmental_score']
            assert results['overall_efficiency'] == mock_fastapi_response['efficiency']['overall_efficiency']

    @pytest.mark.asyncio
    async def test_error_handling(self, service, mock_process_input):
        """Test error handling in FastAPI service"""
        process = await Process.objects.acreate(
            technical_params=mock_process_input['technical_params'],
            economic_params=mock_process_input['economic_params'],
            environmental_params=mock_process_input['environmental_params']
        )

        with patch.object(service.technical_integrator, 'analyze_technical', new_callable=AsyncMock) as mock_technical:
            mock_technical.side_effect = Exception("Technical analysis failed")
            
            with pytest.raises(Exception) as exc_info:
                await service.analyze_process(process.id)
            
            assert "Technical analysis failed" in str(exc_info.value)
            assert process.status == 'failed'

    @pytest.mark.asyncio
    async def test_status_tracking(self, service, mock_process_input):
        """Test analysis status tracking"""
        process = await Process.objects.acreate(
            technical_params=mock_process_input['technical_params']
        )

        # Test status updates
        await service._update_status(process.id, 'processing', 25)
        updated_process = await Process.objects.aget(id=process.id)
        assert updated_process.status == 'processing'
        assert updated_process.progress == 25

    @pytest.mark.asyncio
    async def test_results_storage(self, service, mock_process_input, mock_fastapi_response):
        """Test analysis results storage"""
        process = await Process.objects.acreate(
            technical_params=mock_process_input['technical_params']
        )

        # Store results
        await service._store_results(
            process.id,
            mock_fastapi_response['technical'],
            mock_fastapi_response['economic'],
            mock_fastapi_response['environmental'],
            mock_fastapi_response['efficiency']
        )

        # Verify stored results
        results = await AnalysisResults.objects.aget(process_id=process.id)
        assert results.technical_results == mock_fastapi_response['technical']
        assert results.economic_results == mock_fastapi_response['economic']
        assert results.environmental_results == mock_fastapi_response['environmental']
        assert results.efficiency_results == mock_fastapi_response['efficiency'] 