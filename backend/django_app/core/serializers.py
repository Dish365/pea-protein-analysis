from rest_framework import serializers
from .models import Equipment, ProcessStep, Analysis

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class ProcessStepSerializer(serializers.ModelSerializer):
    equipment_details = EquipmentSerializer(source='equipment', read_only=True)
    
    class Meta:
        model = ProcessStep
        fields = '__all__'

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
