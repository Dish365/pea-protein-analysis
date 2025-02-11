from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import httpx
from .models import ProcessAnalysis
from .serializers import ProcessAnalysisSerializer


class ProcessAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ProcessAnalysis.objects.all()
    serializer_class = ProcessAnalysisSerializer

    def perform_create(self, serializer):
        """Create process analysis record"""
        process = serializer.save()
        return process

    @action(detail=True, methods=['post'])
    async def analyze(self, request, pk=None):
        """Trigger analysis pipeline in FastAPI"""
        process = self.get_object()

        try:
            async with httpx.AsyncClient() as client:
                # Call FastAPI analysis pipeline
                response = await client.post(
                    f"{settings.FASTAPI_BASE_URL}/process/analyze",
                    json={
                        "process_id": str(process.id),
                        "process_type": process.process_type,
                        "parameters": request.data
                    }
                )

                if response.status_code == 200:
                    # Update process with results
                    results = response.json()
                    process.status = "completed"
                    process.technical_results = results.get("technical")
                    process.economic_results = results.get("economic")
                    process.environmental_results = results.get(
                        "environmental")
                    process.save()

                    return Response(results)
                else:
                    process.status = "failed"
                    process.save()
                    return Response(
                        {"error": "Analysis failed"},
                        status=500
                    )

        except Exception as e:
            process.status = "failed"
            process.save()
            return Response(
                {"error": str(e)},
                status=500
            )

    @action(detail=True)
    def results(self, request, pk=None):
        """Get analysis results"""
        process = self.get_object()
        return Response({
            'status': process.status,
            'results': {
                'technical': process.technical_results,
                'economic': process.economic_results,
                'environmental': process.environmental_results,
            }
        })

    @action(detail=True)
    def status(self, request, pk=None):
        process = self.get_object()
        return Response({
            'status': process.status,
            'progress': process.progress
        })
