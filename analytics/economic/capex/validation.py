from typing import Dict

class InvalidEquipmentError(ValueError):
    """Exception for invalid equipment configurations"""
    pass

class CapexValidator:
    @staticmethod
    def validate_equipment(equipment: Dict[str, float]):
        required = {'base_cost', 'efficiency_factor', 'installation_complexity'}
        if not required.issubset(equipment.keys()):
            raise InvalidEquipmentError(f"Missing required fields: {required - set(equipment.keys())}")
        
        # New efficiency range validation
        eff = equipment['efficiency_factor']
        if not 0 <= eff <= 1:
            raise InvalidEquipmentError(f"Invalid efficiency_factor {eff} - must be between 0-1") 