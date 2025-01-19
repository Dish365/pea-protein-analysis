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
        technical = results['technical_analysis']
        return {
            'protein_recovery': technical['protein_recovery'],
            'separation_efficiency': technical['separation_efficiency'],
            'process_efficiency': technical['process_efficiency']
        }

    def _get_economic_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key economic metrics for summary"""
        economic = results['economic_analysis']
        return {
            'capex': economic['capex']['total_capex'],
            'opex': economic['opex']['total_opex'],
            'npv': economic['profitability']['metrics']['npv'],
            'roi': economic['profitability']['metrics']['roi']
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
        technical = results['technical_analysis']
        economic = results['economic_analysis']
        environmental = results['environmental_analysis']
        efficiency = results['eco_efficiency_analysis']
        
        return {
            'process': process_id,
            # Technical Results
            'protein_yield': technical['protein_recovery']['yield'],
            'separation_efficiency': technical['separation_efficiency'],
            'particle_size_distribution': {
                'd10': technical['particle_analysis']['d10'],
                'd50': technical['particle_analysis']['d50'],
                'd90': technical['particle_analysis']['d90']
            },
            
            # Economic Results
            'capex': economic['capex_analysis']['total_capex'],
            'opex': economic['opex_analysis']['total_opex'],
            'npv': economic['profitability_analysis']['npv'],
            'roi': economic['profitability_analysis']['roi'],
            
            # Environmental Results
            'gwp': environmental['impact_assessment']['gwp'],
            'hct': environmental['impact_assessment']['hct'],
            'frs': environmental['impact_assessment']['frs'],
            'water_impact': environmental['impact_assessment']['water_consumption'],
            
            # Eco-efficiency Results
            'eco_efficiency_index': efficiency['efficiency_metrics']['eco_efficiency_index'],
            'relative_performance': efficiency['performance_indicators']['relative_performance']
        } 