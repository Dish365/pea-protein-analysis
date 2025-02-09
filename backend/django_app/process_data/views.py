from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProcessAnalysis
from .serializers import ProcessAnalysisSerializer
from .tasks import analyze_process


class ProcessAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ProcessAnalysis.objects.all()
    serializer_class = ProcessAnalysisSerializer

    def perform_create(self, serializer):
        process = serializer.save()
        # Trigger Celery task
        analyze_process.delay(process.id)

    @action(detail=True)
    def results(self, request, pk=None):
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
