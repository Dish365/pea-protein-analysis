from rest_framework import serializers
from .models import ProcessAnalysis, ProcessType


class ProcessAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for ProcessAnalysis model with detailed validation.
    """
    class Meta:
        model = ProcessAnalysis
        fields = [
            'id',
            'type',
            'status',
            'progress',
            'error_message',
            'timestamp',
            'technical_params',
            'economic_params',
            'environmental_params',
            'technical_results',
            'economic_results',
            'environmental_results',
        ] 
        read_only_fields = [
            'id',
            'status',
            'progress',
            'error_message',
            'timestamp',
            'technical_results',
            'economic_results',
            'environmental_results',
        ]

    def validate_technical_params(self, value):
        """Validate technical parameters"""
        required_fields = {
            'processType',
            'airFlowRate',
            'temperature',
            'pressure',
            'inputMass',
            'outputMass',
            'initialProteinContent',
            'targetProteinContent',
        }

        # Check for required fields
        missing_fields = required_fields - set(value.keys())
        if missing_fields:
            raise serializers.ValidationError(
                f"Missing required technical parameters: {', '.join(missing_fields)}"
            )

        # Validate process type
        if value['processType'] not in ['baseline', 'rf', 'ir']:
            raise serializers.ValidationError(
                "Process type must be one of: baseline, rf, ir"
            )

        # Validate numeric fields
        numeric_fields = {
            'airFlowRate': (0, 1000),  # m³/h
            'temperature': (0, 100),    # °C
            'pressure': (0.1, 10),      # bar
            'inputMass': (0, 10000),    # kg
            'outputMass': (0, 10000),   # kg
            'initialProteinContent': (0, 100),  # %
            'targetProteinContent': (0, 100),   # %
        }

        for field, (min_val, max_val) in numeric_fields.items():
            try:
                value_num = float(value[field])
                if not min_val <= value_num <= max_val:
                    raise serializers.ValidationError(
                        f"{field} must be between {min_val} and {max_val}"
                    )
            except (KeyError, ValueError, TypeError):
                raise serializers.ValidationError(
                    f"{field} must be a valid number"
                )

        # Additional process-specific validations
        if value['processType'] == 'rf':
            if not value.get('rfPower', 0) > 0:
                raise serializers.ValidationError(
                    "RF process requires positive RF power"
                )
        elif value['processType'] == 'ir':
            if not value.get('irIntensity', 0) > 0:
                raise serializers.ValidationError(
                    "IR process requires positive IR intensity"
                )

        return value

    def validate_economic_params(self, value):
        """Validate economic parameters"""
        required_fields = {
            'equipmentCost',
            'utilityCost',
            'laborCost',
            'maintenanceCost',
            'productionVolume',
            'operatingHours',
        }

        # Check for required fields
        missing_fields = required_fields - set(value.keys())
        if missing_fields:
            raise serializers.ValidationError(
                f"Missing required economic parameters: {', '.join(missing_fields)}"
            )

        # Validate numeric fields
        numeric_fields = {
            'equipmentCost': (0, None),      # No upper limit for costs
            'utilityCost': (0, None),
            'laborCost': (0, None),
            'maintenanceCost': (0, None),
            'productionVolume': (0, None),
            'operatingHours': (0, 8760),     # Max hours in a year
        }

        for field, limits in numeric_fields.items():
            try:
                value_num = float(value[field])
                if limits[0] is not None and value_num < limits[0]:
                    raise serializers.ValidationError(
                        f"{field} must be greater than {limits[0]}"
                    )
                if limits[1] is not None and value_num > limits[1]:
                    raise serializers.ValidationError(
                        f"{field} must be less than {limits[1]}"
                    )
            except (KeyError, ValueError, TypeError):
                raise serializers.ValidationError(
                    f"{field} must be a valid number"
                )

        return value

    def validate_environmental_params(self, value):
        """Validate environmental parameters"""
        required_fields = {
            'electricityConsumption',
            'waterConsumption',
            'wasteGeneration',
            'co2Emissions',
        }

        # Check for required fields
        missing_fields = required_fields - set(value.keys())
        if missing_fields:
            raise serializers.ValidationError(
                f"Missing required environmental parameters: {', '.join(missing_fields)}"
            )

        # Validate numeric fields
        numeric_fields = {
            'electricityConsumption': (0, None),  # kWh
            'waterConsumption': (0, None),        # m³
            'wasteGeneration': (0, None),         # kg
            'co2Emissions': (0, None),            # kg CO2e
        }

        for field, limits in numeric_fields.items():
            try:
                value_num = float(value[field])
                if value_num < 0:
                    raise serializers.ValidationError(
                        f"{field} cannot be negative"
                    )
            except (KeyError, ValueError, TypeError):
                raise serializers.ValidationError(
                    f"{field} must be a valid number"
                )

        return value

    def validate(self, data):
        """Cross-field validation"""
        # Ensure output mass is less than or equal to input mass
        if (data.get('technical_params', {}).get('outputMass', 0) >
                data.get('technical_params', {}).get('inputMass', 0)):
            raise serializers.ValidationError(
                "Output mass cannot be greater than input mass"
            )

        # Ensure target protein content is achievable
        if (data.get('technical_params', {}).get('targetProteinContent', 0) <
                data.get('technical_params', {}).get('initialProteinContent', 0)):
            raise serializers.ValidationError(
                "Target protein content must be greater than initial content"
            )

        return data
