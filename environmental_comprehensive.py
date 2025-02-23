import requests
import json
import logging
import math
from pprint import pprint
from typing import Dict, Any, Tuple, List

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Process data
process_data = {
    # RF Pretreatment Parameters
    "rf_electricity_kwh": 150.0,          # RF unit power consumption
    "rf_temperature_outfeed_c": 84.4,     # Outfeed temperature
    "rf_temperature_electrode_c": 100.1,   # Electrode temperature
    "rf_frequency_mhz": 27.12,            # RF frequency
    "rf_anode_current_a": 1.79,           # Anode current
    "rf_grid_current_a": 0.56,            # Grid current
    
    # Process Steps Energy Consumption
    "air_classifier_milling_kwh": 250.0,   # ~21% contribution
    "air_classification_kwh": 250.0,       # ~21% contribution
    "hammer_milling_kwh": 150.0,          # ~13% contribution
    "dehulling_kwh": 150.0,               # ~16% contribution
    
    # Water and Moisture Management
    "tempering_water_kg": 800.0,          # Reduced water need due to RF
    "initial_moisture_content": 0.136,     # 13.6% initial
    "final_moisture_content": 0.102,       # 10.2% after RF
    "target_moisture_content": 0.125,      # 12.5% target for dehulling
    
    # Production Parameters
    "product_kg": 1500.0,                 # Daily production capacity
    "equipment_kg": 8500.0,               # Total equipment mass
    "waste_kg": 450.0,                    # Daily waste generation
    "transport_ton_km": 1200.0,           # Transportation of materials
    
    # Process Configuration
    "conveyor_speed_m_min": 0.17,         # RF conveyor speed
    "material_depth_mm": 30.0,            # RF material bed depth
    "electrode_gap_mm": 86.9,             # RF electrode gap
    "thermal_ratio": 0.65                 # Thermal processing ratio
}

# Allocation parameters
allocation_params = {
    "allocation_method": "economic",       # Default method as per research
    "product_values": {
        "protein_concentrate": 6.50,       # Higher value protein product
        "starch": 2.30,                   # Starch-rich fraction
        "fiber": 1.80                     # Hull/fiber fraction
    },
    "mass_flows": {
        "protein_concentrate": 219.0,      # 21.9% yield for RF treatment
        "starch": 600.0,                  # Starch fraction yield
        "fiber": 181.0                    # Fiber/hull fraction yield
    },
    "hybrid_weights": {
        "economic": 0.6,                  # Economic allocation weight
        "physical": 0.4                   # Physical allocation weight
    }
}

def validate_mass_balance(process_data: Dict[str, float], allocation_params: Dict[str, Any]) -> List[str]:
    """Validate mass balance between process input and allocated products
    
    Args:
        process_data: Process input parameters
        allocation_params: Allocation parameters including mass flows
        
    Returns:
        List of warning messages if any validation issues found
    """
    warnings = []
    
    # Check total mass balance
    total_process_mass = process_data["product_kg"]
    total_products_mass = sum(allocation_params["mass_flows"].values())
    
    if not math.isclose(total_process_mass, total_products_mass, rel_tol=0.01):
        msg = (f"Mass balance mismatch: process total {total_process_mass} kg != "
               f"products total {total_products_mass} kg")
        warnings.append(msg)
        logger.warning(msg)
    
    # Check protein yield against research benchmark (21.9% ± 2%)
    protein_yield = (allocation_params["mass_flows"]["protein_concentrate"] / 
                    total_products_mass if total_products_mass > 0 else 0)
    
    if not (0.199 <= protein_yield <= 0.239):
        msg = (f"Protein yield {protein_yield:.3%} outside expected range "
               f"(19.9%-23.9%) for RF treatment")
        warnings.append(msg)
        logger.warning(msg)
        
    return warnings

def validate_energy_balance(process_data: Dict[str, float]) -> List[str]:
    """Validate energy distribution and total consumption
    
    Args:
        process_data: Process input parameters
        
    Returns:
        List of warning messages if any validation issues found
    """
    warnings = []
    
    # Calculate total energy consumption
    total_energy = (
        process_data["rf_electricity_kwh"] +
        process_data["air_classifier_milling_kwh"] +
        process_data["air_classification_kwh"] +
        process_data["hammer_milling_kwh"] +
        process_data["dehulling_kwh"]
    )
    
    # Check total energy against research value
    if not math.isclose(total_energy, 950.0, rel_tol=0.01):
        msg = f"Total energy {total_energy:.1f} kWh differs from research value (950.0 kWh)"
        warnings.append(msg)
        logger.warning(msg)
    
    # Validate process step contributions
    energy_contributions = {
        "air_classifier_milling": process_data["air_classifier_milling_kwh"] / total_energy,
        "air_classification": process_data["air_classification_kwh"] / total_energy,
        "rf_treatment": process_data["rf_electricity_kwh"] / total_energy,
        "hammer_milling": process_data["hammer_milling_kwh"] / total_energy,
        "dehulling": process_data["dehulling_kwh"] / total_energy
    }
    
    # Expected contributions from research
    expected_contributions = {
        "air_classifier_milling": 0.21,  # 21%
        "air_classification": 0.21,      # 21%
        "rf_treatment": 0.19,           # 19%
        "hammer_milling": 0.13,         # 13%
        "dehulling": 0.16              # 16%
    }
    
    for step, contribution in energy_contributions.items():
        expected = expected_contributions[step]
        if not math.isclose(contribution, expected, abs_tol=0.02):  # Allow 2% deviation
            msg = (f"{step} energy contribution {contribution:.1%} differs from "
                  f"expected {expected:.1%}")
            warnings.append(msg)
            logger.warning(msg)
            
    return warnings

def validate_process_data(process_data: Dict[str, float], 
                        allocation_params: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate process data against research benchmarks
    
    Args:
        process_data: Process input parameters
        allocation_params: Allocation parameters
        
    Returns:
        Tuple of (is_valid: bool, warnings: List[str])
    """
    warnings = []
    
    # Collect warnings from mass balance validation
    warnings.extend(validate_mass_balance(process_data, allocation_params))
    
    # Collect warnings from energy balance validation
    warnings.extend(validate_energy_balance(process_data))
    
    # Validate RF-specific parameters
    if not (80 <= process_data["rf_temperature_outfeed_c"] <= 90):
        msg = (f"RF outfeed temperature {process_data['rf_temperature_outfeed_c']}°C "
               f"outside optimal range (80-90°C)")
        warnings.append(msg)
        logger.warning(msg)
        
    if not (95 <= process_data["rf_temperature_electrode_c"] <= 105):
        msg = (f"RF electrode temperature {process_data['rf_temperature_electrode_c']}°C "
               f"outside optimal range (95-105°C)")
        warnings.append(msg)
        logger.warning(msg)
    
    moisture_reduction = (process_data["initial_moisture_content"] - 
                        process_data["final_moisture_content"])
    if not (0.03 <= moisture_reduction <= 0.04):
        msg = (f"Moisture reduction {moisture_reduction:.3f} outside expected "
               f"range (0.03-0.04)")
        warnings.append(msg)
        logger.warning(msg)
    
    # Return validation result
    is_valid = len(warnings) == 0
    return is_valid, warnings

def print_environmental_results(results: Dict[str, Any]) -> None:
    """Pretty print the environmental analysis results"""
    print("\n=== Comprehensive Environmental Analysis Results ===\n")
    
    # Impact Results
    print("Environmental Impacts:")
    impacts = results.get('impact_results', {}).get('total_impacts', {})
    print(f"Global Warming Potential (GWP): {impacts.get('gwp', 0):.2f} kg CO2 eq")
    print(f"Human Carcinogenic Toxicity (HCT): {impacts.get('hct', 0):.2e} CTUh")
    print(f"Fossil Resource Scarcity (FRS): {impacts.get('frs', 0):.2f} kg oil eq")
    print(f"Water Consumption: {impacts.get('water_consumption', 0):.2f} kg")

    # Process Contributions
    if 'process_contributions' in results.get('impact_results', {}):
        print("\nProcess Contributions:")
        contributions = results['impact_results']['process_contributions']
        for impact_type, processes in contributions.items():
            print(f"\n{impact_type.upper()} Contributions:")
            for process, data in processes.items():
                print(f"  {process}: {data.get('value', 0):.2f} {data.get('unit', '')}")

    # RF Validation Results
    if 'rf_validation' in results:
        print("\nRF Treatment Validation:")
        rf_val = results['rf_validation']
        
        # Temperature
        print("\nTemperature Parameters:")
        for temp_type, data in rf_val.get('temperature', {}).items():
            print(f"  {temp_type.title()}:")
            print(f"    Value: {data.get('value', 0):.1f}°C")
            print(f"    Within Range: {'Yes' if data.get('within_range') else 'No'}")
            print(f"    Optimal: {data.get('optimal', 0):.1f}°C")
            print(f"    Tolerance: {data.get('tolerance', '')}")
        
        # Moisture
        print("\nMoisture Parameters:")
        moisture = rf_val.get('moisture', {})
        print(f"  Initial: {moisture.get('initial', 0):.3f}")
        print(f"  Final: {moisture.get('final', 0):.3f}")
        print(f"  Reduction: {moisture.get('reduction', 0):.3f}")
        print(f"  Within Range: {'Yes' if moisture.get('within_range') else 'No'}")
        print(f"  Optimal Reduction: {moisture.get('optimal_reduction', 0):.3f}")
        
        # Energy Efficiency
        energy = rf_val.get('energy_efficiency', {})
        print("\nEnergy Efficiency:")
        print(f"  Contribution: {energy.get('value', 0):.1%}")
        print(f"  Within Range: {'Yes' if energy.get('within_range') else 'No'}")
        print(f"  Optimal: {energy.get('optimal', 0):.1%}")

    # Process Metadata
    print("\nProcess Metadata:")
    metadata = results.get('impact_results', {}).get('metadata', {})
    print(f"Total Mass: {metadata.get('total_mass', 0):.2f} kg")
    print(f"Energy Intensity: {metadata.get('energy_intensity', 0):.2f} kWh/kg")
    print(f"Water Intensity: {metadata.get('water_intensity', 0):.2f} kg/kg")
    print(f"Thermal Ratio: {metadata.get('thermal_ratio', 0):.2%}")

    # Allocation Results
    if results.get('allocation_results'):
        print("\nAllocation Results:")
        alloc_results = results['allocation_results']
        
        print("\nAllocation Factors:")
        for product, factor in alloc_results.get('allocation_factors', {}).items():
            print(f"  {product}: {factor:.2%}")
        
        print("\nAllocated Impacts:")
        for product, impacts in alloc_results.get('allocated_impacts', {}).items():
            print(f"\n{product}:")
            for impact_type, value in impacts.items():
                print(f"  {impact_type}: {value:.2f}")

    # Suggested Method
    print(f"\nSuggested Allocation Method: {results.get('suggested_allocation_method', 'Not provided')}")

def handle_error_response(response: requests.Response) -> None:
    """Handle error responses from the API"""
    try:
        error_data = response.json()
        logger.error(f"API Error Response: {error_data}")
        if isinstance(error_data, dict):
            detail = error_data.get('detail', {})
            if isinstance(detail, dict):
                print(f"Error Type: {detail.get('type', 'Unknown')}")
                print(f"Message: {detail.get('message', 'No message provided')}")
            else:
                print(f"Error: {detail}")
        else:
            print(f"Error: {error_data}")
    except json.JSONDecodeError:
        print(f"Error: {response.text}")

def main():
    """Main function to run the environmental analysis"""
    try:
        # Validate process data before making request
        is_valid, warnings = validate_process_data(process_data, allocation_params)
        
        if not is_valid:
            print("\nWarnings detected in process data:")
            for warning in warnings:
                print(f"- {warning}")
            
            # Ask for confirmation to proceed
            proceed = input("\nProceed with analysis despite warnings? (y/n): ").lower()
            if proceed != 'y':
                print("Analysis cancelled.")
                return
        
        # Prepare request payload
        request_payload = {
            "request": process_data,
            "allocation_method": allocation_params["allocation_method"],
            "product_values": allocation_params["product_values"],
            "mass_flows": allocation_params["mass_flows"],
            "hybrid_weights": allocation_params["hybrid_weights"]
        }

        # Log request details
        logger.debug("Request URL: http://localhost:8001/api/v1/environmental/impact/analyze-process")
        logger.debug(f"Request Payload: {json.dumps(request_payload, indent=2)}")

        # Make the request to the environmental analysis endpoint
        response = requests.post(
            "http://localhost:8001/api/v1/environmental/impact/analyze-process",
            json=request_payload,
            params={"include_contributions": True}
        )

        # Log response details
        logger.debug(f"Response Status: {response.status_code}")
        logger.debug(f"Response Headers: {dict(response.headers)}")

        # Check if request was successful
        if response.status_code == 200:
            results = response.json()
            logger.debug(f"Response Body: {json.dumps(results, indent=2)}")
            print_environmental_results(results)
            
            # Save results to file for reference
            with open('environmental_analysis_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print("\nDetailed results saved to 'environmental_analysis_results.json'")
        else:
            print(f"\nError {response.status_code}:")
            handle_error_response(response)
            # Log raw response for debugging
            logger.error(f"Raw Response: {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        print(f"Request failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
