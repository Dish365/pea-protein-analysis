from rest_framework import serializers
from ..models.process import ProcessAnalysis, AnalysisResult, ProcessType

class ProcessAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for ProcessAnalysis model.
    Basic validation only - complex validations handled by model and FastAPI endpoints.
    """
    class Meta:
        model = ProcessAnalysis
        fields = [
            # Basic Info
            'id', 'process_type', 'timestamp', 'status', 'progress',
            
            # Technical Parameters
            'input_mass', 'output_mass',
            'initial_protein_content', 'final_protein_content',
            'initial_moisture_content', 'final_moisture_content',
            'moisture_reduction',
            'd10_particle_size', 'd50_particle_size', 'd90_particle_size',
            'air_flow', 'classifier_speed',
            
            # Multi-stage Process Data
            'process_stages', 'target_protein_content', 'stage_efficiencies',
            
            # Economic Parameters
            'equipment_cost', 'maintenance_cost',
            'raw_material_cost', 'utility_cost', 'labor_cost',
            'project_duration', 'discount_rate', 'production_volume',
            'installation_factor', 'indirect_costs_factor', 'maintenance_factor',
            'monte_carlo_iterations', 'uncertainty',
            'indirect_factors',
            'equipment_efficiency',
            'hours_per_week', 'weeks_per_year', 'num_workers',
            
            # Revenue Parameters
            'selling_price', 'market_growth_rate', 'price_volatility',
            'revenue',
            
            # Environmental Parameters
            'electricity_consumption', 'cooling_consumption', 'water_consumption'
        ]
        read_only_fields = ['id', 'timestamp', 'status', 'progress', 'moisture_reduction']

    def to_representation(self, instance):
        """Convert model instance to JSON-serializable format"""
        data = super().to_representation(instance)
        
        # Ensure numeric fields are properly formatted
        numeric_fields = [
            'input_mass', 'output_mass',
            'initial_protein_content', 'final_protein_content',
            'initial_moisture_content', 'final_moisture_content',
            'moisture_reduction',
            'd10_particle_size', 'd50_particle_size', 'd90_particle_size',
            'equipment_cost', 'maintenance_cost', 'raw_material_cost',
            'utility_cost', 'labor_cost', 'discount_rate',
            'production_volume', 'equipment_efficiency'
        ]
        
        for field in numeric_fields:
            if field in data and data[field] is not None:
                data[field] = float(data[field])
        
        return data


class AnalysisResultSerializer(serializers.ModelSerializer):
    """
    Serializer for AnalysisResult model.
    Handles serialization of analysis results.
    """
    class Meta:
        model = AnalysisResult
        fields = [
            'id', 'process', 'timestamp',
            'technical_results', 'economic_results',
            'environmental_results', 'efficiency_results'
        ]
        read_only_fields = ['id', 'timestamp']

    def to_representation(self, instance):
        """Convert model instance to JSON-serializable format"""
        data = super().to_representation(instance)
        
        # Ensure JSON fields are properly formatted
        json_fields = [
            'technical_results', 'economic_results',
            'environmental_results', 'efficiency_results'
        ]
        
        for field in json_fields:
            if field in data and data[field] is None:
                data[field] = {}
        
        return data


class ProcessInputSerializer(serializers.Serializer):
    """
    Serializer for process analysis input.
    Basic validation only - complex validations handled by FastAPI endpoints.
    """
    # Technical Inputs
    process_type = serializers.ChoiceField(choices=[pt.value for pt in ProcessType])
    input_mass = serializers.FloatField(min_value=0)
    output_mass = serializers.FloatField(min_value=0)
    initial_protein_content = serializers.FloatField(min_value=0, max_value=100)
    final_protein_content = serializers.FloatField(min_value=0, max_value=100)
    initial_moisture_content = serializers.FloatField(min_value=0, max_value=100)
    final_moisture_content = serializers.FloatField(min_value=0, max_value=100)
    d10_particle_size = serializers.FloatField(min_value=0)
    d50_particle_size = serializers.FloatField(min_value=0)
    d90_particle_size = serializers.FloatField(min_value=0)
    
    # Economic Inputs
    equipment_cost = serializers.FloatField(min_value=0)
    maintenance_cost = serializers.FloatField(min_value=0)
    raw_material_cost = serializers.FloatField(min_value=0)
    utility_cost = serializers.FloatField(min_value=0)
    labor_cost = serializers.FloatField(min_value=0)
    project_duration = serializers.IntegerField(min_value=1)
    discount_rate = serializers.FloatField(min_value=0, max_value=1)
    production_volume = serializers.FloatField(min_value=0)
    equipment_efficiency = serializers.FloatField(min_value=0, max_value=1, default=0.85)
    hours_per_week = serializers.IntegerField(min_value=1, max_value=168, default=40)
    weeks_per_year = serializers.IntegerField(min_value=1, max_value=52, default=52)
    num_workers = serializers.IntegerField(min_value=1, default=1)
    
    # Environmental Inputs
    electricity_consumption = serializers.FloatField(min_value=0)
    cooling_consumption = serializers.FloatField(min_value=0)
    water_consumption = serializers.FloatField(min_value=0)
    
    # Optional Inputs
    revenue = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        required=False,
        allow_empty=True
    )
    indirect_factors = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_empty=True
    ) 