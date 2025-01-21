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
from typing import Dict, Any
from django.core.cache import cache
import asyncio
import httpx

logger = logging.getLogger(__name__)

class ProcessAnalysisView(APIView):
    """
    Process Analysis API View
    
    Handles the complete lifecycle of process analysis:
    1. Input validation and process creation
    2. Analysis execution
    3. Results storage and retrieval
    """
    
    def post(self, request, *args, **kwargs):
        """Handle new process analysis request"""
        try:
            # Validate input data
            serializer = ProcessInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid input data', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create process analysis record
            process = ProcessAnalysis.objects.create(
                **serializer.validated_data,
                status='pending',
                progress=0
            )

            # Initialize FastAPI service and execute analysis
            async def run_analysis():
                try:
                    async with FastAPIService() as service:
                        return await service.analyze_process(serializer.validated_data)
                except Exception as e:
                    logger.error(f"FastAPI service error: {str(e)}", exc_info=True)
                    raise  # Re-raise to be caught by outer try

            # Run the analysis using asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                results = loop.run_until_complete(run_analysis())
                if results is None:
                    raise RuntimeError("Analysis failed with no results")
            except Exception as e:
                # Update process status to failed
                process.status = 'failed'
                process.save()
                
                error_msg = str(e)
                if isinstance(e, RuntimeError):
                    error_msg = e.args[0] if e.args else "Service error"
                
                # Update cache with error status
                cache_key = f"process_analysis_{process.id}"
                cache.set(cache_key, {
                    'status': 'failed',
                    'error': error_msg
                }, timeout=3600)
                
                logger.error(f"Analysis failed: {error_msg}", exc_info=True)
                return Response(
                    {'error': error_msg},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                loop.close()
                try:
                    asyncio.set_event_loop(None)
                except Exception:
                    pass  # Ignore any errors when cleaning up the event loop

            # Prepare and store results
            try:
                result_data = self._prepare_result_data(process, results)
                analysis_result = AnalysisResult.objects.create(**result_data)
            except Exception as e:
                process.status = 'failed'
                process.save()
                error_msg = f"Failed to store analysis results: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return Response(
                    {'error': error_msg},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Update process status
            process.status = 'completed'
            process.progress = 100
            process.save()
            
            # Prepare response with summary
            response_data = {
                'process_id': process.id,
                'status': 'success',
                'message': 'Analysis completed successfully',
                'summary': {
                    'technical': self._get_technical_summary(results),
                    'economic': self._get_economic_summary(results),
                    'environmental': self._get_environmental_summary(results, serializer.validated_data),
                    'efficiency': self._get_efficiency_summary(results)
                }
            }
            
            # Update cache
            cache_key = f"process_analysis_{process.id}"
            cache.set(cache_key, {
                'status': 'completed',
                'progress': 100,
                'message': 'Analysis completed successfully'
            }, timeout=3600)
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Analysis failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, process_id=None, *args, **kwargs):
        """Get analysis results or list of analyses"""
        try:
            if process_id:
                # Get specific analysis
                process = ProcessAnalysis.objects.get(id=process_id)
                serializer = ProcessAnalysisSerializer(process)
                return Response(serializer.data)
            else:
                # List all analyses
                processes = ProcessAnalysis.objects.all().order_by('-timestamp')[:10]
                serializer = ProcessAnalysisSerializer(processes, many=True)
                return Response(serializer.data)
                
        except ProcessAnalysis.DoesNotExist:
            return Response(
                {'error': 'Process analysis not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Failed to retrieve analysis: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Failed to retrieve analysis', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _prepare_result_data(self, process: ProcessAnalysis, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare analysis results for storage"""
        # Extract results from the summary if present
        if 'summary' in results:
            technical = results['summary'].get('technical', {})
            economic = results['summary'].get('economic', {})
            environmental = results['summary'].get('environmental', {})
            efficiency = results['summary'].get('efficiency', {})
        else:
            technical = results.get('technical_results', {})
            economic = results.get('economic_analysis', {})
            environmental = results.get('environmental_results', {})
            efficiency = results.get('efficiency_results', {})
        
        return {
            'process': process,
            'technical_results': technical,
            'economic_results': economic,
            'environmental_results': environmental,
            'efficiency_results': efficiency
        }

    def _get_technical_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key technical metrics for summary"""
        technical = results.get('technical_results', {})
        environmental = results.get('environmental_results', {})
        
        # Get base technical metrics
        summary = {
            'protein_recovery': technical.get('protein_recovery', {}),
            'separation_efficiency': technical.get('separation_efficiency', 0),
            'process_efficiency': technical.get('process_efficiency', 0),
            'particle_size_distribution': technical.get('particle_size_distribution', {})
        }

        # Add consumption metrics from either technical or environmental results
        electricity = technical.get('electricity_consumption')
        if electricity is None:
            electricity = environmental.get('electricity_consumption')
        
        cooling = technical.get('cooling_consumption')
        if cooling is None:
            cooling = environmental.get('cooling_consumption')
            
        water = technical.get('water_consumption')
        if water is None:
            water = environmental.get('water_consumption')

        # Add metrics if they exist
        if electricity is not None:
            summary['electricity_consumption'] = electricity
        if cooling is not None:
            summary['cooling_consumption'] = cooling
        if water is not None:
            summary['water_consumption'] = water

        return summary

    def _get_economic_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key economic metrics for summary"""
        economic = results.get('economic_analysis', {})
        return {
            'capex_analysis': economic.get('capex_analysis', {}).get('summary', {}),
            'opex_analysis': economic.get('opex_analysis', {}).get('summary', {}),
            'profitability_analysis': economic.get('profitability_analysis', {}).get('metrics', {})
        }

    def _get_environmental_summary(self, results: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key environmental metrics for summary
        
        Args:
            results: Analysis results from the FastAPI service
            input_data: Original input data from the request
            
        Returns:
            Dict containing impact assessment and consumption metrics
        """
        # Extract environmental results from the nested structure
        env_results = results.get('environmental_results', {})
        environmental = env_results.get('environmental_results', env_results)

        # Get consumption metrics
        consumption_metrics = environmental.get('consumption_metrics', {
            'electricity': None,
            'cooling': None,
            'water': None
        })

        # For RF and IR process types, ensure consumption metrics are properly set
        process_type = input_data.get('process_type')
        if process_type == 'rf' and 'electricity_consumption' in input_data:
            consumption_metrics['electricity'] = input_data['electricity_consumption']
        elif process_type == 'ir' and 'cooling_consumption' in input_data:
            consumption_metrics['cooling'] = input_data['cooling_consumption']

        return {
            'impact_assessment': environmental.get('impact_assessment', {
                'gwp': 0.0,
                'hct': 0.0,
                'frs': 0.0
            }),
            'consumption_metrics': consumption_metrics
        }

    def _get_efficiency_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key efficiency metrics for summary"""
        efficiency = results.get('efficiency_results', {})
        return {
            'efficiency_metrics': efficiency.get('efficiency_metrics', {}),
            'performance_indicators': efficiency.get('performance_indicators', {})
        }