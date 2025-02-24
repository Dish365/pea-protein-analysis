import requests
import json
import logging
from pprint import pprint
from typing import Dict, Any, List, Optional
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProcessType(str, Enum):
    BASELINE = 'baseline'
    RF = 'rf'
    IR = 'ir'

# Process data for protein analysis
process_data = {
    # Protein Recovery Parameters
    "recovery_input": {
        "initial_protein_content": 45.0,    # Initial protein content (%)
        "output_protein_content": 63.1,     # RF treatment protein purity (%)
        "input_mass": 1000.0,              # Input mass (kg)
        "output_mass": 219.0,              # Output mass based on 21.9% yield
        "process_type": ProcessType.RF,      # RF treatment process
        "initial_moisture": 13.6,            # 13.6% initial moisture
        "final_moisture": 10.2,             # 10.2% after RF treatment
        "moisture_compensation_factor": 0.05  # Example moisture compensation factor
    },
    
    # Separation Parameters
    "separation_input": {
        "feed_composition": {
            "protein": 45.0,
            "starch": 35.0,
            "fiber": 15.0,
            "others": 5.0
        },
        "product_composition": {
            "protein": 63.1,               # RF treatment protein purity
            "starch": 22.9,
            "fiber": 10.0,
            "others": 4.0
        },
        "mass_flow": {
            "input": 1000.0,              # Total input mass
            "output": 219.0               # Mass of protein concentrate (21.9% yield)
        },
        "process_data": [
            {
                "feed_composition": "feed_composition",      # Reference to top-level feed composition
                "product_composition": "product_composition", # Reference to top-level product composition
                "mass_flow": "mass_flow"         # Reference to top-level mass flow
            }
        ],
        "target_purity": 63.1              # Target protein purity for RF treatment
    },
    
    # Particle Size Parameters
    "particle_input": {
        # From Table 2 - RF Treatment values for fine fraction (proteins)
        "particle_sizes": [2.42, 7.14, 17.85],  # D0.1, D0.5, D0.9 for fine fraction
        "weights": [0.1, 0.5, 0.4],            # Distribution weights
        "density": 1.35,                       # Typical pea protein density g/cm³
        "initial_moisture": 13.6,              # 13.6% initial moisture
        "final_moisture": 10.2,               # 10.2% after RF treatment
        "treatment_type": ProcessType.RF,       # RF treatment
        "target_ranges": {
            "D10": (2.0, 3.0),                # Around measured D0.1 of 2.42
            "D50": (7.0, 7.5),                # Around measured D0.5 of 7.14
            "D90": (17.0, 18.0),              # Around measured D0.9 of 17.85
            "span": (1.5, 2.5)                # Typical range for protein concentrate
        },
        "percentiles": {
            "d10": 2.42,  # D0.1 value
            "d50": 7.14,  # D0.5 value
            "d90": 17.85  # D0.9 value
        }
    }
}

def validate_protein_recovery_data(recovery_data: Dict[str, Any]) -> List[str]:
    """Validate protein recovery input data
    
    Args:
        recovery_data: Protein recovery parameters
        
    Returns:
        List of warning messages if any validation issues found
    """
    warnings = []
    
    # Check protein content ranges
    if not (0 < recovery_data["initial_protein_content"] < 100):
        warnings.append(f"Initial protein content {recovery_data['initial_protein_content']}% outside valid range (0-100%)")
    
    if not (0 < recovery_data["output_protein_content"] < 100):
        warnings.append(f"Output protein content {recovery_data['output_protein_content']}% outside valid range (0-100%)")
    
    if recovery_data["output_protein_content"] <= recovery_data["initial_protein_content"]:
        warnings.append("Output protein content should be higher than initial content for concentration process")
    
    # Check mass balance
    if recovery_data["output_mass"] >= recovery_data["input_mass"]:
        warnings.append("Output mass should be less than input mass due to separation process")
    
    # Check process type
    if recovery_data["process_type"] not in ["baseline", "rf", "ir"]:
        warnings.append(f"Invalid process type: {recovery_data['process_type']}")
    
    return warnings

def validate_separation_data(separation_data: Dict[str, Any]) -> List[str]:
    """Validate separation efficiency input data
    
    Args:
        separation_data: Separation efficiency parameters
        
    Returns:
        List of warning messages if any validation issues found
    """
    warnings = []
    
    # Check composition totals
    feed_total = sum(separation_data["feed_composition"].values())
    if not (99.5 <= feed_total <= 100.5):
        warnings.append(f"Feed composition total {feed_total}% should sum to 100%")
    
    product_total = sum(separation_data["product_composition"].values())
    if not (99.5 <= product_total <= 100.5):
        warnings.append(f"Product composition total {product_total}% should sum to 100%")
    
    # Check mass balance
    mass_in = separation_data["mass_flow"]["input"]
    mass_out = separation_data["mass_flow"]["output"]
    if mass_out > mass_in:
        warnings.append(f"Output mass ({mass_out} kg) cannot exceed input mass ({mass_in} kg)")
    
    # Check process data references
    if separation_data.get("process_data"):
        required_refs = {"feed_composition", "product_composition", "mass_flow"}
        for stage in separation_data["process_data"]:
            # Check that all required references are present
            missing_refs = required_refs - set(stage.keys())
            if missing_refs:
                warnings.append(f"Missing required references in process data: {missing_refs}")
            
            # Check that references point to valid top-level keys
            for ref_key in stage:
                if ref_key in required_refs and stage[ref_key] not in separation_data:
                    warnings.append(f"Invalid reference '{stage[ref_key]}' in process data")
    
    return warnings

def validate_particle_data(particle_data: Dict[str, Any]) -> List[str]:
    """Validate particle size analysis input data
    
    Args:
        particle_data: Particle size analysis parameters
        
    Returns:
        List of warning messages if any validation issues found
    """
    warnings = []
    
    # Check particle size distribution
    if len(particle_data["particle_sizes"]) != len(particle_data["weights"]):
        warnings.append("Particle sizes and weights arrays must have same length")
    
    weight_sum = sum(particle_data["weights"])
    if not (0.99 <= weight_sum <= 1.01):
        warnings.append(f"Particle size weights sum {weight_sum} should be approximately 1.0")
    
    # Check moisture content (in percentage)
    if not (0 <= particle_data["initial_moisture"] <= 100):
        warnings.append(f"Initial moisture {particle_data['initial_moisture']}% outside valid range (0-100%)")
    
    if not (0 <= particle_data["final_moisture"] <= 100):
        warnings.append(f"Final moisture {particle_data['final_moisture']}% outside valid range (0-100%)")
    
    if particle_data["final_moisture"] >= particle_data["initial_moisture"]:
        warnings.append("Final moisture should be less than initial moisture after processing")
    
    # Check treatment type
    if particle_data["treatment_type"] not in ["baseline", "rf", "ir"]:
        warnings.append(f"Invalid treatment type: {particle_data['treatment_type']}")
    
    # Check target ranges
    if "target_ranges" in particle_data:
        valid_keys = {"D10", "D50", "D90", "span"}
        for key in particle_data["target_ranges"]:
            if key.lower() not in valid_keys:
                warnings.append(f"Invalid target range key: {key}")
            range_tuple = particle_data["target_ranges"][key]
            if not isinstance(range_tuple, tuple) or len(range_tuple) != 2:
                warnings.append(f"Target range {key} must be a tuple of (min, max)")
            elif range_tuple[0] >= range_tuple[1]:
                warnings.append(f"Target range {key} min value must be less than max value")
    
    return warnings

def print_technical_results(results: Dict[str, Any]) -> None:
    """Pretty print the technical analysis results"""
    print("\n=== Comprehensive Technical Analysis Results ===\n")
    
    # Recovery Metrics
    if "recovery_metrics" in results:
        print("Protein Recovery Metrics:")
        recovery = results["recovery_metrics"]
        print(f"Recovery Rate: {recovery.get('recovery_rate', 0):.2f}%")
        print(f"Protein Loss: {recovery.get('protein_loss', 0):.2f} kg")
        print(f"Process Efficiency: {recovery.get('process_efficiency', 0):.2f}%")
    
    # Separation Metrics
    if "separation_metrics" in results:
        print("\nSeparation Efficiency Metrics:")
        separation = results["separation_metrics"]
        
        if "component_recoveries" in separation:
            print("\nComponent Recoveries:")
            for component, recovery in separation["component_recoveries"].items():
                print(f"  {component}: {recovery:.2f}%")
        
        if "cumulative_efficiency" in separation:
            print(f"\nCumulative Efficiency: {separation['cumulative_efficiency']:.2f}%")
            print(f"Average Step Efficiency: {separation.get('average_step_efficiency', 0):.2f}%")
            print(f"Purity Achievement: {separation.get('purity_achievement', 0):.2f}%")
    
    # Particle Metrics
    if "particle_metrics" in results:
        print("\nParticle Size Analysis:")
        particle = results["particle_metrics"]
        
        if "distribution_parameters" in particle:
            dist = particle["distribution_parameters"]
            print("\nDistribution Parameters:")
            print(f"D10: {dist.get('d10', 0):.2f} μm")
            print(f"D50: {dist.get('d50', 0):.2f} μm")
            print(f"D90: {dist.get('d90', 0):.2f} μm")
            print(f"Span: {dist.get('span', 0):.2f}")
        
        if "quality_metrics" in particle:
            print("\nQuality Metrics:")
            quality = particle["quality_metrics"]
            print(f"Size Distribution Score: {quality.get('size_score', 0):.2f}")
            print(f"Uniformity Index: {quality.get('uniformity', 0):.2f}")
    
    # Process Performance
    if "process_performance" in results and results["process_performance"]:
        print("\nOverall Process Performance:")
        performance = results["process_performance"]
        print(f"Cumulative Efficiency: {performance.get('cumulative_efficiency', 0):.2f}%")
        print(f"Average Step Efficiency: {performance.get('average_step_efficiency', 0):.2f}%")
        print(f"Purity Achievement: {performance.get('purity_achievement', 0):.2f}%")

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
    """Main function to run the technical analysis"""
    try:
        # Validate all input data
        recovery_warnings = validate_protein_recovery_data(process_data["recovery_input"])
        separation_warnings = validate_separation_data(process_data["separation_input"])
        particle_warnings = validate_particle_data(process_data["particle_input"])
        
        all_warnings = recovery_warnings + separation_warnings + particle_warnings
        
        if all_warnings:
            print("\nWarnings detected in process data:")
            for warning in all_warnings:
                print(f"- {warning}")
            
            # Ask for confirmation to proceed
            proceed = input("\nProceed with analysis despite warnings? (y/n): ").lower()
            if proceed != 'y':
                print("Analysis cancelled.")
                return
        
        # Log request details
        logger.debug("Request URL: http://localhost:8001/api/v1/protein/protein-analysis/complete-analysis/")
        logger.debug(f"Request Payload: {json.dumps(process_data, indent=2)}")

        # Update the request payload with new moisture parameters
        response = requests.post(
            "http://localhost:8001/api/v1/protein/protein-analysis/complete-analysis/",
            json={
                "recovery_input": {
                    "initial_protein_content": process_data["recovery_input"]["initial_protein_content"],
                    "output_protein_content": process_data["recovery_input"]["output_protein_content"],
                    "input_mass": process_data["recovery_input"]["input_mass"],
                    "output_mass": process_data["recovery_input"]["output_mass"],
                    "process_type": process_data["recovery_input"]["process_type"].value,
                    "initial_moisture": process_data["recovery_input"].get("initial_moisture", 13.6),
                    "final_moisture": process_data["recovery_input"].get("final_moisture", 10.2),
                    "moisture_compensation_factor": process_data["recovery_input"].get("moisture_compensation_factor", 0.05)
                },
                "separation_input": {
                    **process_data["separation_input"],
                     "process_data": [
                        {
                            **step,
                            "processing_moisture": 10.2  # Add as direct value
                        }
                        for step in process_data["separation_input"]["process_data"]
                    ]
                },
                "particle_input": {
                    **process_data["particle_input"],
                    "treatment_type": process_data["particle_input"]["treatment_type"].value,
                    "percentiles": {
                        "d10": process_data["particle_input"]["particle_sizes"][0],
                        "d50": process_data["particle_input"]["particle_sizes"][1],
                        "d90": process_data["particle_input"]["particle_sizes"][2]
                    }
                }
            }
        )

        # Log response details
        logger.debug(f"Response Status: {response.status_code}")
        logger.debug(f"Response Headers: {dict(response.headers)}")

        # Check if request was successful
        if response.status_code == 200:
            results = response.json()
            logger.debug(f"Response Body: {json.dumps(results, indent=2)}")
            print_technical_results(results)
            
            # Save results to file for reference
            with open('technical_analysis_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print("\nDetailed results saved to 'technical_analysis_results.json'")
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
