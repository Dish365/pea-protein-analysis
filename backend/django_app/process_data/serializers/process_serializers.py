from rest_framework import serializers
from ..models.process import ProcessAnalysis, AnalysisResult, ProcessType

class ProcessAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for ProcessAnalysis model.
    Matches test data structure from test_fastapi_service.py
    """
    class Meta:
        model = ProcessAnalysis
        fields = [
            # Basic Info
            'id', 'process_type', 'timestamp', 'status', 'progress',
            
            # Technical Analysis Inputs
            # Process Parameters
            'air_flow', 'classifier_speed',
            
            # Mass Balance
            'input_mass', 'output_mass',
            
            # Content Analysis
            'initial_protein_content', 'final_protein_content',
            'initial_moisture_content', 'final_moisture_content',
            
            # Particle Size Analysis
            'd10_particle_size', 'd50_particle_size', 'd90_particle_size',
            
            # Economic Analysis Inputs
            # Equipment and Costs
            'equipment', 'equipment_cost', 'maintenance_cost',
            'installation_factor', 'indirect_costs_factor', 'maintenance_factor',
            'indirect_factors',
            
            # Operating Costs
            'raw_material_cost', 'utility_cost', 'labor_cost',
            
            # Resource Configuration
            'utilities', 'raw_materials', 'labor_config',
            
            # Financial Parameters
            'project_duration', 'discount_rate', 'production_volume',
            'revenue_per_year', 'cash_flows',
            
            # Risk Analysis
            'sensitivity_range', 'steps',
            
            # Environmental Analysis
            'electricity_consumption', 'cooling_consumption',
            'water_consumption', 'transport_consumption',
            'equipment_mass', 'thermal_ratio',
            
            # Energy Data
            'energy_consumption',
            
            # Production Data
            'production_data', 'product_values',
            
            # Allocation Configuration
            'allocation_method', 'hybrid_weights'
        ]
        read_only_fields = ['id', 'timestamp', 'status', 'progress']

    def to_representation(self, instance):
        """Convert model instance to JSON-serializable format"""
        data = super().to_representation(instance)
        
        # Ensure numeric fields are properly formatted
        numeric_fields = [
            'input_mass', 'output_mass',
            'initial_protein_content', 'final_protein_content',
            'initial_moisture_content', 'final_moisture_content',
            'd10_particle_size', 'd50_particle_size', 'd90_particle_size',
            'equipment_cost', 'maintenance_cost',
            'raw_material_cost', 'utility_cost', 'labor_cost',
            'installation_factor', 'indirect_costs_factor', 'maintenance_factor',
            'project_duration', 'discount_rate', 'production_volume',
            'revenue_per_year',
            'sensitivity_range', 'steps',
            'electricity_consumption', 'cooling_consumption',
            'water_consumption', 'transport_consumption',
            'equipment_mass', 'thermal_ratio',
            'air_flow', 'classifier_speed'
        ]
        
        for field in numeric_fields:
            if field in data and data[field] is not None:
                data[field] = float(data[field])
        
        # Ensure JSON fields are properly formatted
        json_fields = [
            'equipment', 'indirect_factors',
            'utilities', 'raw_materials', 'labor_config',
            'cash_flows', 'energy_consumption',
            'production_data', 'product_values',
            'hybrid_weights'
        ]
        
        for field in json_fields:
            if field in data and data[field] is None:
                data[field] = {}
        
        return data


class AnalysisResultSerializer(serializers.ModelSerializer):
    """
    Serializer for AnalysisResult model.
    Matches test response structure from test_fastapi_service.py
    """
    class Meta:
        model = AnalysisResult
        fields = [
            'id', 'process', 'timestamp',
            'technical_results',
            'economic_results',
            'environmental_results',
            'efficiency_results'
        ]
        read_only_fields = ['id', 'timestamp']

    def to_representation(self, instance):
        """Convert model instance to JSON-serializable format"""
        data = super().to_representation(instance)
        
        # Extract results from the root level
        technical_results = data.pop('technical_results', {})
        economic_results = data.pop('economic_results', {})
        environmental_results = data.pop('environmental_results', {})
        efficiency_results = data.pop('efficiency_results', {})
        
        # Create summary structure
        summary = {
            'technical': technical_results,
            'economic': economic_results,
            'environmental': environmental_results,
            'efficiency': efficiency_results
        }
        
        # Handle environmental section specially to preserve structure
        if isinstance(summary['environmental'].get('environmental_results', {}), dict):
            env_results = summary['environmental'].pop('environmental_results', {})
            summary['environmental'].update(env_results)
        
        data['summary'] = summary
        data['status'] = 'success'
        data['message'] = 'Analysis completed successfully'
        
        return data


class ProcessInputSerializer(serializers.Serializer):
    """
    Serializer for process analysis input validation.
    Matches test input structure from test_fastapi_service.py
    """
    # Basic Info
    process_type = serializers.ChoiceField(choices=[pt.value for pt in ProcessType])
    
    # Process Parameters
    air_flow = serializers.FloatField(min_value=0)
    classifier_speed = serializers.FloatField(min_value=0)
    
    # Mass Balance
    input_mass = serializers.FloatField(min_value=0)
    output_mass = serializers.FloatField(min_value=0)
    
    # Content Analysis
    initial_protein_content = serializers.FloatField(min_value=0, max_value=100)
    final_protein_content = serializers.FloatField(min_value=0, max_value=100)
    initial_moisture_content = serializers.FloatField(min_value=0, max_value=100)
    final_moisture_content = serializers.FloatField(min_value=0, max_value=100)
    
    # Particle Size Analysis
    d10_particle_size = serializers.FloatField(min_value=0)
    d50_particle_size = serializers.FloatField(min_value=0)
    d90_particle_size = serializers.FloatField(min_value=0)
    
    # Equipment and Costs
    equipment = serializers.JSONField()
    equipment_cost = serializers.FloatField(min_value=0)
    maintenance_cost = serializers.FloatField(min_value=0)
    installation_factor = serializers.FloatField(min_value=0, max_value=1, default=0.2)
    indirect_costs_factor = serializers.FloatField(min_value=0, max_value=1, default=0.15)
    maintenance_factor = serializers.FloatField(min_value=0, max_value=1, default=0.05)
    indirect_factors = serializers.JSONField()
    
    # Operating Costs
    raw_material_cost = serializers.FloatField(min_value=0)
    utility_cost = serializers.FloatField(min_value=0)
    labor_cost = serializers.FloatField(min_value=0)
    
    # Resource Configuration
    utilities = serializers.JSONField()
    raw_materials = serializers.JSONField()
    labor_config = serializers.JSONField()
    
    # Financial Parameters
    project_duration = serializers.IntegerField(min_value=1)
    discount_rate = serializers.FloatField(min_value=0, max_value=1)
    production_volume = serializers.FloatField(min_value=0)
    revenue_data = serializers.DictField(child=serializers.FloatField())
    economic_factors = serializers.DictField()
    
    # Risk Analysis
    sensitivity_range = serializers.FloatField(min_value=0, max_value=1, default=0.2)
    steps = serializers.IntegerField(min_value=1, default=10)
    
    # Environmental Analysis
    electricity_consumption = serializers.FloatField(min_value=0)
    cooling_consumption = serializers.FloatField(min_value=0)
    water_consumption = serializers.FloatField(min_value=0)
    transport_consumption = serializers.FloatField(min_value=0)
    equipment_mass = serializers.FloatField(min_value=0)
    thermal_ratio = serializers.FloatField(min_value=0, max_value=1, default=0.3)
    energy_consumption = serializers.JSONField()
    
    # Production Data
    production_data = serializers.JSONField()
    product_values = serializers.JSONField()
    
    # Allocation Configuration
    allocation_method = serializers.ChoiceField(
        choices=['economic', 'physical', 'hybrid'],
        default='hybrid'
    )
    hybrid_weights = serializers.JSONField()

    def validate(self, data):
        """
        Validate process type specific requirements
        """
        process_type = data.get('process_type')
        
        if process_type == 'rf':
            if data.get('electricity_consumption', 0) <= 0:
                raise serializers.ValidationError({
                    'electricity_consumption': 'RF process requires positive electricity consumption'
                })
        elif process_type == 'ir':
            if data.get('cooling_consumption', 0) <= 0:
                raise serializers.ValidationError({
                    'cooling_consumption': 'IR process requires positive cooling consumption'
                })
        
        return data


class TechnicalInputSerializer(serializers.Serializer):
    """
    Serializer for technical analysis input validation.
    """
    # Process Parameters
    air_flow = serializers.FloatField(min_value=0)
    classifier_speed = serializers.FloatField(min_value=0)
    
    # Mass Balance
    input_mass = serializers.FloatField(min_value=0)
    output_mass = serializers.FloatField(min_value=0)
    
    # Content Analysis
    initial_protein_content = serializers.FloatField(min_value=0, max_value=100)
    final_protein_content = serializers.FloatField(min_value=0, max_value=100)
    initial_moisture_content = serializers.FloatField(min_value=0, max_value=100)
    final_moisture_content = serializers.FloatField(min_value=0, max_value=100)
    
    # Particle Size Analysis
    d10_particle_size = serializers.FloatField(min_value=0)
    d50_particle_size = serializers.FloatField(min_value=0)
    d90_particle_size = serializers.FloatField(min_value=0)


class EconomicInputSerializer(serializers.Serializer):
    """
    Serializer for economic analysis input validation.
    Matches the structure in economic.py
    """
    # Equipment Configuration
    equipment = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )

    # Resource Configuration
    utilities = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )

    raw_materials = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )

    labor_config = serializers.DictField()
    revenue_data = serializers.DictField()
    economic_factors = serializers.DictField()

    # Process Type and Analysis Parameters
    process_type = serializers.ChoiceField(choices=['baseline', 'rf', 'ir'])
    monte_carlo_iterations = serializers.IntegerField(
        min_value=100, 
        max_value=10000, 
        default=1000
    )
    uncertainty = serializers.FloatField(
        min_value=0, 
        max_value=1, 
        default=0.1
    )

    # Add validation for new indirect costs field
    indirect_costs = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=[]
    )

    def validate_equipment(self, value):
        """Validate equipment structure"""
        required_fields = ['name', 'base_cost', 'processing_capacity',
                         'energy_consumption', 'maintenance_factor']
        for item in value:
            missing = [field for field in required_fields if field not in item]
            if missing:
                raise serializers.ValidationError(
                    f"Missing required fields for equipment: {', '.join(missing)}"
                )
        return value

    def validate_utilities(self, value):
        """Validate utilities structure"""
        required_fields = ['name', 'consumption', 'unit_price', 'unit']
        for item in value:
            missing = [field for field in required_fields if field not in item]
            if missing:
                raise serializers.ValidationError(
                    f"Missing required fields for utility: {', '.join(missing)}"
                )
        return value

    def validate_raw_materials(self, value):
        """Validate raw materials structure"""
        required_fields = ['name', 'quantity', 'unit_price', 'unit']
        for item in value:
            missing = [field for field in required_fields if field not in item]
            if missing:
                raise serializers.ValidationError(
                    f"Missing required fields for raw material: {', '.join(missing)}"
                )
        return value

    def validate_labor_config(self, value):
        """Validate labor configuration"""
        required_fields = ['hourly_wage', 'hours_per_week', 'weeks_per_year', 'num_workers']
        missing = [field for field in required_fields if field not in value]
        if missing:
            raise serializers.ValidationError(
                f"Missing required fields for labor config: {', '.join(missing)}"
            )
        if value.get('hours_per_week', 0) > 168:
            raise serializers.ValidationError("Hours per week cannot exceed 168")
        if value.get('weeks_per_year', 0) > 52:
            raise serializers.ValidationError("Weeks per year cannot exceed 52")
        if value.get('num_workers', 0) < 1:
            raise serializers.ValidationError("Number of workers must be at least 1")
        return value

    def validate_revenue_data(self, value):
        """Validate revenue data"""
        required_fields = ['product_price', 'annual_production']
        missing = [field for field in required_fields if field not in value]
        if missing:
            raise serializers.ValidationError(
                f"Missing required fields for revenue data: {', '.join(missing)}"
            )
        return value

    def validate_economic_factors(self, value):
        """Validate economic factors"""
        required_fields = ['installation_factor', 'indirect_costs_factor', 'maintenance_factor',
                         'project_duration', 'discount_rate', 'production_volume']
        missing = [field for field in required_fields if field not in value]
        if missing:
            raise serializers.ValidationError(
                f"Missing required fields for economic factors: {', '.join(missing)}"
            )
        if not 0 <= value.get('installation_factor', 0) <= 1:
            raise serializers.ValidationError("Installation factor must be between 0 and 1")
        if not 0 <= value.get('indirect_costs_factor', 0) <= 1:
            raise serializers.ValidationError("Indirect costs factor must be between 0 and 1")
        if not 0 <= value.get('maintenance_factor', 0) <= 1:
            raise serializers.ValidationError("Maintenance factor must be between 0 and 1")
        if not 0 <= value.get('discount_rate', 0) <= 1:
            raise serializers.ValidationError("Discount rate must be between 0 and 1")
        if value.get('project_duration', 0) < 1:
            raise serializers.ValidationError("Project duration must be at least 1 year")
        if value.get('production_volume', 0) <= 0:
            raise serializers.ValidationError("Production volume must be positive")
        return value

    def validate_indirect_costs(self, value):
        """Validate indirect costs structure"""
        required_fields = ['name', 'cost', 'percentage']
        for item in value:
            missing = [field for field in required_fields if field not in item]
            if missing:
                raise serializers.ValidationError(
                    f"Missing required fields for indirect cost: {', '.join(missing)}"
                )
        return value


class EnvironmentalInputSerializer(serializers.Serializer):
    """
    Serializer for environmental analysis input validation.
    """
    # Environmental Analysis
    electricity_consumption = serializers.FloatField(min_value=0)
    cooling_consumption = serializers.FloatField(min_value=0)
    water_consumption = serializers.FloatField(min_value=0)
    transport_consumption = serializers.FloatField(min_value=0)
    equipment_mass = serializers.FloatField(min_value=0)
    thermal_ratio = serializers.FloatField(min_value=0, max_value=1, default=0.3)
    energy_consumption = serializers.JSONField()
    
    # Production Data
    production_data = serializers.JSONField()
    product_values = serializers.JSONField()
    
    # Allocation Configuration
    allocation_method = serializers.ChoiceField(
        choices=['economic', 'physical', 'hybrid'],
        default='hybrid'
    )
    hybrid_weights = serializers.JSONField() 