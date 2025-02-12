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
        
        # Define expected nested structures from test data
        expected_structure = {
            'summary': {
                'technical': {
                    'protein_recovery': {
                        'mass': 0.0,
                        'content': 0.0,
                        'yield': 0.0
                    },
                    'separation_efficiency': 0.0,
                    'process_efficiency': 0.0,
                    'particle_size_distribution': {
                        'd10': 0.0,
                        'd50': 0.0,
                        'd90': 0.0
                    }
                },
                'economic': {
                    'capex_analysis': {
                        'total_capex': 0.0,
                        'equipment_cost': 0.0,
                        'installation_cost': 0.0,
                        'indirect_cost': 0.0
                    },
                    'opex_analysis': {
                        'total_opex': 0.0,
                        'utilities_cost': 0.0,
                        'materials_cost': 0.0,
                        'labor_cost': 0.0,
                        'maintenance_cost': 0.0
                    },
                    'profitability_analysis': {
                        'npv': 0.0,
                        'roi': 0.0
                    }
                },
                'environmental': {
                    'impact_assessment': {
                        'gwp': 0.0,
                        'hct': 0.0,
                        'frs': 0.0
                    },
                    'consumption_metrics': {
                        'electricity': None,
                        'cooling': None,
                        'water': None
                    }
                },
                'efficiency': {
                    'efficiency_metrics': {
                        'eco_efficiency_index': 0.0
                    },
                    'performance_indicators': {
                        'relative_performance': 0.0
                    }
                }
            }
        }
        
        # Transform results into summary structure
        summary = {
            'technical': data.pop('technical_results', {}),
            'economic': data.pop('economic_results', {}),
            'environmental': data.pop('environmental_results', {}),
            'efficiency': data.pop('efficiency_results', {})
        }
        
        # Merge with expected structure
        for section, structure in expected_structure['summary'].items():
            if section in summary:
                if section == 'environmental':
                    # Deep merge for environmental section to preserve consumption_metrics
                    env_data = summary[section]
                    env_structure = structure.copy()  # Create a copy to avoid modifying the original
                    
                    # Update impact assessment if present
                    if 'impact_assessment' in env_data:
                        env_structure['impact_assessment'].update(env_data.get('impact_assessment', {}))
                    
                    # Update consumption metrics if present
                    if 'consumption_metrics' in env_data:
                        env_structure['consumption_metrics'].update(env_data.get('consumption_metrics', {}))
                    elif isinstance(env_data.get('environmental_results', {}), dict):
                        # Handle nested environmental_results structure
                        env_results = env_data.get('environmental_results', {})
                        if 'consumption_metrics' in env_results:
                            env_structure['consumption_metrics'].update(env_results['consumption_metrics'])
                    
                    summary[section] = env_structure
                else:
                    summary[section] = {**structure, **summary[section]}
        
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
    revenue_per_year = serializers.FloatField(min_value=0)
    cash_flows = serializers.JSONField()
    
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
    """
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
    revenue_per_year = serializers.FloatField(min_value=0)
    cash_flows = serializers.JSONField()
    
    # Risk Analysis
    sensitivity_range = serializers.FloatField(min_value=0, max_value=1, default=0.2)
    steps = serializers.IntegerField(min_value=1, default=10)


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