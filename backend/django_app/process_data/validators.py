from django.core.exceptions import ValidationError

def validate_equipment_structure(value):
    """Validate equipment JSON structure"""
    required_fields = ['name', 'base_cost', 'efficiency_factor', 'installation_complexity',
                      'maintenance_cost', 'energy_consumption', 'processing_capacity']
    
    if not isinstance(value, list):
        raise ValidationError("Equipment must be a list")
        
    for equipment in value:
        missing_fields = [field for field in required_fields if field not in equipment]
        if missing_fields:
            raise ValidationError(f"Missing required equipment fields: {', '.join(missing_fields)}") 