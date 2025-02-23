import requests
import json
import logging
from pprint import pprint
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Process data
process_data = {
    "electricity_kwh": 950.0,         # Matching economic analysis electricity consumption
    "cooling_kwh": 250.0,             # Cooling energy for protein preservation
    "water_kg": 3500.0,               # Process water consumption
    "transport_ton_km": 1200.0,       # Transportation of raw materials and products
    "product_kg": 1500.0,             # Daily production capacity
    "equipment_kg": 8500.0,           # Total equipment mass
    "waste_kg": 450.0,                # Daily waste generation
    "thermal_ratio": 0.65             # 65% thermal processing
}

# Allocation parameters
allocation_params = {
    "allocation_method": "hybrid",        # Can be "physical", "economic", or "hybrid"
    "product_values": {
        "protein_isolate": 6.50,          # Matching economic analysis product price
        "starch": 2.30,
        "fiber": 1.80
    },
    "mass_flows": {
        "protein_isolate": 1000.0,
        "starch": 300.0,
        "fiber": 200.0
    },
    "hybrid_weights": {
        "economic": 0.6,
        "physical": 0.4
    }
}

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

    # Metadata
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
