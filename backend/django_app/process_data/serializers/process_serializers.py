from rest_framework import serializers
from ..models.process import ProcessAnalysis, AnalysisResult, ProcessType

class ProcessAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessAnalysis
        fields = '__all__'
        read_only_fields = ('timestamp', 'moisture_reduction')
        
    def validate(self, data):
        """Validate process-specific constraints"""
        if data['process_type'] not in [pt.value for pt in ProcessType]:
            raise serializers.ValidationError({
                'process_type': f"Invalid process type. Must be one of: {', '.join([pt.value for pt in ProcessType])}"
            })
            
        # Process-specific validations
        if data['process_type'] == ProcessType.RF.value:
            if data.get('electricity_consumption', 0) <= 0:
                raise serializers.ValidationError({
                    'electricity_consumption': "RF treatment requires positive electricity consumption"
                })
            if data.get('initial_moisture_content', 0) < 13.6:
                raise serializers.ValidationError({
                    'initial_moisture_content': "RF treatment requires ≥13.6% initial moisture content"
                })
        elif data['process_type'] == ProcessType.IR.value:
            if data.get('cooling_consumption', 0) <= 0:
                raise serializers.ValidationError({
                    'cooling_consumption': "IR treatment requires positive cooling consumption"
                })
            if abs(data.get('initial_moisture_content', 0) - 15.5) > 0.5:
                raise serializers.ValidationError({
                    'initial_moisture_content': "IR treatment requires ~15.5% initial moisture content"
                })
                
        # Mass balance validation
        if data['output_mass'] > data['input_mass']:
            raise serializers.ValidationError({
                'output_mass': "Output mass cannot exceed input mass"
            })
            
        # Content range validations
        for field in ['initial_protein_content', 'final_protein_content', 
                     'initial_moisture_content', 'final_moisture_content']:
            if not (0 <= data[field] <= 100):
                raise serializers.ValidationError({
                    field: f"{field} must be between 0-100%"
                })
                
        if data['final_moisture_content'] > data['initial_moisture_content']:
            raise serializers.ValidationError({
                'final_moisture_content': "Final moisture content cannot be higher than initial moisture content"
            })
            
        # Particle size validations
        particle_sizes = [
            data['d10_particle_size'],
            data['d50_particle_size'],
            data['d90_particle_size']
        ]
        if not all(size > 0 for size in particle_sizes):
            raise serializers.ValidationError("All particle sizes must be positive")
            
        if not (data['d10_particle_size'] <= data['d50_particle_size'] <= data['d90_particle_size']):
            raise serializers.ValidationError("Particle sizes must be in order: D10 ≤ D50 ≤ D90")
            
        # Economic parameter validations
        if not (0 < data['discount_rate'] < 1):
            raise serializers.ValidationError({
                'discount_rate': "Discount rate must be between 0 and 1"
            })
            
        economic_fields = [
            'equipment_cost', 'maintenance_cost', 'raw_material_cost',
            'utility_cost', 'labor_cost', 'production_volume'
        ]
        for field in economic_fields:
            if data[field] <= 0:
                raise serializers.ValidationError({
                    field: f"{field} must be positive"
                })
                
        if data['project_duration'] <= 0:
            raise serializers.ValidationError({
                'project_duration': "Project duration must be positive"
            })
                
        return data

class AnalysisResultSerializer(serializers.ModelSerializer):
    process_type = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalysisResult
        fields = '__all__'
        read_only_fields = ('timestamp',)
        
    def get_process_type(self, obj):
        return obj.process.process_type
        
    def validate(self, data):
        """Validate analysis results"""
        # Validate percentage fields
        percentage_fields = ['protein_recovery', 'separation_efficiency', 
                           'process_efficiency', 'roi']
        for field in percentage_fields:
            if field in data and data[field] is not None:
                if not (0 <= data[field] <= 100):
                    raise serializers.ValidationError({
                        field: f"{field} must be between 0-100%"
                    })
                    
        # Validate non-negative fields
        non_negative_fields = [
            'npv', 'payback_period', 'profitability_index',
            'gwp', 'hct', 'frs', 'water_consumption',
            'eco_efficiency_index'
        ]
        for field in non_negative_fields:
            if field in data and data[field] is not None:
                if data[field] < 0:
                    raise serializers.ValidationError({
                        field: f"{field} cannot be negative"
                    })
                    
        # Validate JSON fields
        if data.get('particle_size_distribution'):
            required_keys = ['d10', 'd50', 'd90']
            if not all(key in data['particle_size_distribution'] for key in required_keys):
                raise serializers.ValidationError({
                    'particle_size_distribution': "Must include d10, d50, and d90"
                })
                
        if data.get('capex'):
            required_keys = ['equipment_cost', 'installation_cost', 
                           'indirect_cost', 'total_capex']
            if not all(key in data['capex'] for key in required_keys):
                raise serializers.ValidationError({
                    'capex': "Must include all cost components"
                })
                
        if data.get('opex'):
            required_keys = ['utilities_cost', 'materials_cost', 
                           'labor_cost', 'maintenance_cost', 'total_opex']
            if not all(key in data['opex'] for key in required_keys):
                raise serializers.ValidationError({
                    'opex': "Must include all cost components"
                })
                
        if data.get('allocated_impacts'):
            required_keys = ['method', 'factors', 'results']
            if not all(key in data['allocated_impacts'] for key in required_keys):
                raise serializers.ValidationError({
                    'allocated_impacts': "Must include method, factors, and results"
                })
                
        return data

class ProcessInputSerializer(serializers.Serializer):
    # Technical Inputs
    process_type = serializers.ChoiceField(choices=ProcessType.choices())
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
    
    # Environmental Inputs
    electricity_consumption = serializers.FloatField(min_value=0)
    cooling_consumption = serializers.FloatField(min_value=0)
    water_consumption = serializers.FloatField(min_value=0)

    def validate(self, data):
        """Custom validation for interdependent fields"""
        if data['output_mass'] > data['input_mass']:
            raise serializers.ValidationError("Output mass cannot be greater than input mass")
        
        if data['d10_particle_size'] > data['d50_particle_size'] or \
           data['d50_particle_size'] > data['d90_particle_size']:
            raise serializers.ValidationError("Particle size distribution must be d10 ≤ d50 ≤ d90")
            
        # Process-specific validations
        if data['process_type'] == ProcessType.RF.value:
            if data['electricity_consumption'] <= 0:
                raise serializers.ValidationError({
                    'electricity_consumption': "RF treatment requires positive electricity consumption"
                })
        elif data['process_type'] == ProcessType.IR.value:
            if data['cooling_consumption'] <= 0:
                raise serializers.ValidationError({
                    'cooling_consumption': "IR treatment requires positive cooling consumption"
                })
        
        # Moisture content validations
        if data['final_moisture_content'] > data['initial_moisture_content']:
            raise serializers.ValidationError({
                'final_moisture_content': "Final moisture content cannot be higher than initial moisture content"
            })
            
        # Process-specific moisture validations
        if data['process_type'] in [ProcessType.RF.value, ProcessType.IR.value]:
            min_reduction = 5.0  # Minimum 5% moisture reduction for RF/IR treatments
            moisture_reduction = data['initial_moisture_content'] - data['final_moisture_content']
            if moisture_reduction < min_reduction:
                raise serializers.ValidationError({
                    'final_moisture_content': f"RF/IR treatments require minimum {min_reduction}% moisture reduction"
                })
        
        return data 