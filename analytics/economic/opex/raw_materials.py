from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

def calculate_raw_material_costs(
    raw_materials: List[Dict[str, float]],
    production_volume: float,
    reference_volume: Optional[float] = None
) -> Dict[str, Any]:
    """
    Calculate raw material costs with proper scaling based on production volume.
    
    Args:
        raw_materials: List of raw material configurations
            Each material must have:
            - name: Material name
            - quantity: Base quantity required
            - unit_price: Cost per unit
            - unit: Unit of measurement
            - protein_content: Optional protein content (for pea flour)
        production_volume: Current production volume
        reference_volume: Reference production volume for base quantities
            
    Returns:
        Dictionary containing:
        - total_cost: Total annual raw material costs
        - materials_breakdown: Detailed cost breakdown by material
        
    Raises:
        ValueError: If raw materials list is empty or contains invalid data
    """
    if not raw_materials:
        raise ValueError("Raw materials list cannot be empty")
        
    if production_volume <= 0:
        raise ValueError("Production volume must be positive")
        
    # Use current volume as reference if not provided
    reference_volume = reference_volume or production_volume
    if reference_volume <= 0:
        raise ValueError("Reference volume must be positive")
        
    # Calculate volume ratio for scaling
    volume_ratio = production_volume / reference_volume
    
    total_cost = 0.0
    materials_breakdown = []
    
    for material in raw_materials:
        # Validate required fields
        required_fields = ["name", "quantity", "unit_price", "unit"]
        if not all(field in material for field in required_fields):
            raise ValueError(f"Material must contain all required fields: {required_fields}")
            
        # Scale quantity based on production volume
        base_quantity = material["quantity"]
        scaled_quantity = base_quantity * volume_ratio
        
        # Calculate cost
        unit_price = material["unit_price"]
        material_cost = scaled_quantity * unit_price
        
        # Add to total
        total_cost += material_cost
        
        # Store breakdown info
        material_info = {
            "name": material["name"],
            "base_quantity": base_quantity,
            "scaled_quantity": scaled_quantity,
            "unit_price": unit_price,
            "unit": material["unit"],
            "total_cost": material_cost
        }
        
        # Add protein content info if available and valid
        if "protein_content" in material and material["protein_content"] is not None:
            try:
                protein_content = float(material["protein_content"])
                if 0 <= protein_content <= 1:  # Validate protein content is a valid percentage
                    material_info["protein_content"] = protein_content
                    material_info["protein_yield"] = scaled_quantity * protein_content
            except (ValueError, TypeError):
                # Log warning but continue processing
                logger.warning(f"Invalid protein content for material {material['name']}")
            
        materials_breakdown.append(material_info)
    
    return {
        "total_cost": total_cost,
        "materials_breakdown": materials_breakdown
    }
