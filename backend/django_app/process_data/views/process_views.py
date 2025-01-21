from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.process import ProcessAnalysis, AnalysisResult
from ..serializers.process_serializers import (
    ProcessAnalysisSerializer,
    ProcessInputSerializer,
    AnalysisResultSerializer
)
from ..services.fastapi_service import FastAPIService
import logging
from typing import Dict, Any, Optional
from django.core.cache import cache

logger = logging.getLogger(__name__)

class ProcessAnalysisView(APIView):
    """
    Process Analysis API View
    
    Handles the complete lifecycle of process analysis:
    1. Input validation and process creation
    2. Analysis execution with progress tracking
    3. Results storage and retrieval
    4. Status monitoring and updates
    """
    
    ANALYSIS_STAGES = {
        'VALIDATION': {'weight': 5, 'message': 'Validating input data'},
        'TECHNICAL': {'weight': 25, 'message': 'Performing technical analysis'},
        'ECONOMIC': {'weight': 25, 'message': 'Performing economic analysis'},
        'ENVIRONMENTAL': {'weight': 25, 'message': 'Performing environmental analysis'},
        'EFFICIENCY': {'weight': 15, 'message': 'Calculating eco-efficiency metrics'},
        'SAVING': {'weight': 5, 'message': 'Saving analysis results'}
    }
    
    async def post(self, request):
        """
        Handle new process analysis request.
        
        Flow:
        1. Validate input data
        2. Create process record
        3. Execute analysis pipeline
        4. Store results
        5. Return comprehensive response
        """
        try:
            # Stage 1: Input Validation
            process_id = await self._validate_and_create_process(request.data)
            cache_key = f"process_analysis_{process_id}"
            
            try:
                # Stage 2: Analysis Execution
                async with FastAPIService() as fastapi_service:
                    results = await self._execute_analysis_pipeline(
                        fastapi_service,
                        request.data,
                        process_id,
                        cache_key
                    )
                
                # Stage 3: Results Processing
                response_data = await self._process_and_store_results(
                    process_id,
                    results,
                    cache_key
                )
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                await self._handle_analysis_failure(process_id, cache_key, str(e))
                raise
                
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Process analysis error: {str(e)}", exc_info=True)
            return Response(
                {'error': f"Analysis failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get(self, request, process_id: Optional[int] = None):
        """
        Retrieve analysis results or status.
        
        Endpoints:
        - GET /process/              : List all processes with basic info
        - GET /process/{id}/         : Get specific process details
        - GET /process/{id}/status/  : Get analysis status and progress
        - GET /process/{id}/results/ : Get complete analysis results
        """
        try:
            if process_id is None:
                return await self._get_process_list()
            
            if 'status' in request.query_params:
                return await self._get_analysis_status(process_id)
            elif 'results' in request.query_params:
                return await self._get_analysis_results(process_id)
            else:
                return await self._get_process_details(process_id)
                
        except ProcessAnalysis.DoesNotExist:
            return Response(
                {'error': 'Process not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving process data: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def _validate_and_create_process(self, data: Dict[str, Any]) -> int:
        """Validate input data and create process record"""
        self._update_progress('VALIDATION', 0)
        
        # Validate input data
        input_serializer = ProcessInputSerializer(data=data)
        if not input_serializer.is_valid():
            raise ValueError(f"Invalid input data: {input_serializer.errors}")
            
        # Create process record
        process_serializer = ProcessAnalysisSerializer(data=input_serializer.validated_data)
        if not process_serializer.is_valid():
            raise ValueError(f"Process validation failed: {process_serializer.errors}")
            
        process = process_serializer.save()
        logger.info(f"Created process analysis record: {process.id}")
        
        self._update_progress('VALIDATION', 100)
        return process.id

    async def _execute_analysis_pipeline(
        self,
        fastapi_service: FastAPIService,
        data: Dict[str, Any],
        process_id: int,
        cache_key: str
    ) -> Dict[str, Any]:
        """Execute the complete analysis pipeline with progress tracking"""
        try:
            # Initialize progress tracking
            cache.set(cache_key, {
                'status': 'processing',
                'stage': 'TECHNICAL',
                'progress': 0,
                'message': self.ANALYSIS_STAGES['TECHNICAL']['message']
            }, timeout=3600)
            
            # Execute analysis
            results = await fastapi_service.analyze_process(data)
            
            return results
            
        except Exception as e:
            logger.error(f"Analysis pipeline failed: {str(e)}", exc_info=True)
            raise

    async def _process_and_store_results(
        self,
        process_id: int,
        results: Dict[str, Any],
        cache_key: str
    ) -> Dict[str, Any]:
        """Process and store analysis results"""
        try:
            self._update_progress('SAVING', 0)
            
            # Prepare result data
            result_data = self._prepare_result_data(process_id, results)
            
            # Validate and save results
            result_serializer = AnalysisResultSerializer(data=result_data)
            if not result_serializer.is_valid():
                raise ValueError(f"Result validation failed: {result_serializer.errors}")
                
            result = result_serializer.save()
            logger.info(f"Saved analysis results for process ID: {process_id}")
            
            # Update cache with completion
            cache.set(cache_key, {
                'status': 'completed',
                'stage': 'COMPLETED',
                'progress': 100,
                'message': 'Analysis completed successfully'
            }, timeout=3600)
            
            # Prepare response
            return {
                'process_id': process_id,
                'status': 'success',
                'results_url': f'/api/process/{process_id}/results/',
                'summary': {
                    'technical': self._get_technical_summary(results),
                    'economic': self._get_economic_summary(results),
                    'environmental': self._get_environmental_summary(results),
                    'efficiency': self._get_efficiency_summary(results)
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing results: {str(e)}", exc_info=True)
            raise

    async def _handle_analysis_failure(
        self,
        process_id: int,
        cache_key: str,
        error_message: str
    ):
        """Handle analysis failure and cleanup"""
        try:
            # Update cache with failure status
            cache.set(cache_key, {
                'status': 'failed',
                'error': error_message
            }, timeout=3600)
            
            # Delete process record
            process = await ProcessAnalysis.objects.aget(id=process_id)
            await process.adelete()
            
            logger.error(f"Analysis failed for process {process_id}: {error_message}")
            
        except Exception as e:
            logger.error(f"Error handling analysis failure: {str(e)}", exc_info=True)

    def _update_progress(self, stage: str, percentage: float):
        """Update progress for current stage"""
        if stage in self.ANALYSIS_STAGES:
            cache.set(self.cache_key, {
                'status': 'processing',
                'stage': stage,
                'progress': percentage,
                'message': self.ANALYSIS_STAGES[stage]['message']
            }, timeout=3600)

    def _get_technical_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key technical metrics for summary"""
        technical = results.get('technical_results', {})
        
        # Extract protein recovery metrics
        protein_metrics = technical.get('recovery_metrics', {})
        recovery_rate = protein_metrics.get('recovery_rate', 0)
        protein_loss = protein_metrics.get('protein_loss', 0)
        concentration_factor = protein_metrics.get('concentration_factor', 0)
        
        # Extract process efficiency metrics
        efficiency_metrics = technical.get('process_efficiency', {})
        process_efficiency = efficiency_metrics.get('process_efficiency', 0)
        yield_gap = efficiency_metrics.get('yield_gap', 0)
        
        return {
            'protein_recovery': {
                'recovery_rate': recovery_rate,
                'protein_loss': protein_loss,
                'concentration_factor': concentration_factor
            },
            'process_efficiency': {
                'efficiency': process_efficiency,
                'yield_gap': yield_gap
            },
            'separation_efficiency': technical.get('separation_efficiency', 0),
            'particle_metrics': technical.get('particle_metrics', {})
        }

    def _get_economic_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key economic metrics for summary"""
        economic = results['economic_analysis']
        
        # Extract CAPEX breakdown
        capex_analysis = economic['capex_analysis']
        capex_summary = {
            'total_capex': capex_analysis['total_capex'],
            'equipment_costs': capex_analysis['equipment_costs'],
            'installation_costs': capex_analysis['installation_costs'],
            'indirect_costs': capex_analysis['indirect_costs']
        }
        
        # Extract OPEX breakdown
        opex_analysis = economic['opex_analysis']
        opex_summary = {
            'total_opex': opex_analysis['total_opex'],
            'utilities_cost': opex_analysis['utilities_cost'],
            'materials_cost': opex_analysis['materials_cost'],
            'labor_cost': opex_analysis['labor_cost'],
            'maintenance_cost': opex_analysis['maintenance_cost']
        }
        
        # Extract profitability metrics
        profitability = economic['profitability_analysis']['metrics']
        profitability_summary = {
            'npv': profitability['npv'],
            'roi': profitability['roi'],
            'payback_period': profitability['payback_period'],
            'discounted_payback': profitability['discounted_payback']
        }
        
        # Extract Monte Carlo results if available
        monte_carlo = economic['profitability_analysis'].get('monte_carlo')
        if monte_carlo:
            profitability_summary.update({
                'monte_carlo_mean': monte_carlo.get('mean_npv'),
                'monte_carlo_std': monte_carlo.get('std_npv'),
                'confidence_interval': monte_carlo.get('confidence_interval')
            })
        
        # Extract cost tracking summary if available
        cost_tracking = economic.get('cost_tracking', {})
        if cost_tracking:
            cost_summary = {
                'total_costs': cost_tracking['cost_summary'].get('total', 0),
                'cost_breakdown': cost_tracking['cost_summary']
            }
        else:
            cost_summary = None
        
        return {
            'capex': capex_summary,
            'opex': opex_summary,
            'profitability': profitability_summary,
            'cost_tracking': cost_summary,
            'process_type': economic.get('process_type', 'baseline'),
            'production_volume': economic.get('production_volume', 0)
        }

    def _get_environmental_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key environmental metrics for summary"""
        environmental = results['environmental_analysis']
        return {
            'gwp': environmental['gwp'],
            'water_consumption': environmental['water_consumption']
        }

    def _get_efficiency_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key efficiency metrics for summary"""
        efficiency = results['eco_efficiency_analysis']
        return {
            'eco_efficiency_index': efficiency['metrics']['eco_efficiency_index'],
            'relative_performance': efficiency['performance']['relative_performance']
        }

    async def _get_process_list(self) -> Response:
        """Get list of all processes with basic info"""
        processes = await ProcessAnalysis.objects.all()
        return Response(ProcessAnalysisSerializer(processes, many=True).data)

    async def _get_process_details(self, process_id: int) -> Response:
        """Get detailed process information"""
        process = await ProcessAnalysis.objects.aget(id=process_id)
        return Response(ProcessAnalysisSerializer(process).data)

    async def _get_analysis_status(self, process_id: int) -> Response:
        """Get current analysis status and progress"""
        cache_key = f"process_analysis_{process_id}"
        status_data = cache.get(cache_key)
        
        if not status_data:
            # Check if analysis is completed
            try:
                result = await AnalysisResult.objects.aget(process_id=process_id)
                status_data = {
                    'status': 'completed',
                    'stage': 'COMPLETED',
                    'progress': 100,
                    'message': 'Analysis completed successfully'
                }
            except AnalysisResult.DoesNotExist:
                status_data = {
                    'status': 'not_found',
                    'message': 'Analysis status not found'
                }
        
        return Response(status_data)

    async def _get_analysis_results(self, process_id: int) -> Response:
        """Get complete analysis results"""
        result = await AnalysisResult.objects.aget(process_id=process_id)
        return Response(AnalysisResultSerializer(result).data)

    def _prepare_result_data(self, process_id: int, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare analysis results for storage"""
        technical = results.get('technical_results', {})
        economic = results.get('economic_analysis', {})
        environmental = results.get('environmental_results', {})
        efficiency = results.get('efficiency_results', {})
        
        # Extract protein recovery metrics
        protein_metrics = technical.get('recovery_metrics', {})
        
        return {
            'process': process_id,
            # Technical Results
            'protein_recovery': {
                'recovery_rate': protein_metrics.get('recovery_rate', 0),
                'protein_loss': protein_metrics.get('protein_loss', 0),
                'concentration_factor': protein_metrics.get('concentration_factor', 0)
            },
            'separation_efficiency': technical.get('separation_efficiency', 0),
            'particle_size_distribution': technical.get('particle_metrics', {
                'd10': 0,
                'd50': 0,
                'd90': 0
            }),
            
            # Economic Results
            'capex': economic.get('capex_analysis', {}).get('total_capex', 0),
            'opex': economic.get('opex_analysis', {}).get('total_opex', 0),
            'npv': economic.get('profitability_analysis', {}).get('npv', 0),
            'roi': economic.get('profitability_analysis', {}).get('roi', 0),
            
            # Environmental Results
            'gwp': environmental.get('impact_assessment', {}).get('gwp', 0),
            'hct': environmental.get('impact_assessment', {}).get('hct', 0),
            'frs': environmental.get('impact_assessment', {}).get('frs', 0),
            'water_impact': environmental.get('impact_assessment', {}).get('water_consumption', 0),
            
            # Eco-efficiency Results
            'eco_efficiency_index': efficiency.get('efficiency_metrics', {}).get('eco_efficiency_index', 0),
            'relative_performance': efficiency.get('performance_indicators', {}).get('relative_performance', 0)
        } 