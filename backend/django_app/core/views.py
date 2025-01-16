from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Equipment, ProcessStep, Analysis
from .serializers import EquipmentSerializer, ProcessStepSerializer, AnalysisSerializer
from users.permissions import IsResearcher, IsAnalyst

# Core views


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated & (IsResearcher | IsAnalyst)]


class ProcessStepViewSet(viewsets.ModelViewSet):
    queryset = ProcessStep.objects.all()
    serializer_class = ProcessStepSerializer
    permission_classes = [IsAuthenticated & (IsResearcher | IsAnalyst)]

    def get_queryset(self):
        queryset = super().get_queryset()
        process_type = self.request.query_params.get("process_type", None)
        if process_type:
            queryset = queryset.filter(process_type=process_type)
        return queryset


class AnalysisViewSet(viewsets.ModelViewSet):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated & (IsResearcher | IsAnalyst)]

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
