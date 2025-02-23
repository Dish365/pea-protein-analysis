"""
Economic Analysis Endpoints Module

This module provides FastAPI endpoints for economic analysis including:
- Capital Expenditure (CAPEX) Analysis
- Operational Expenditure (OPEX) Analysis
- Profitability Analysis
- Business Metrics and Performance Indicators
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

# Configure module logger with full package path
logger = logging.getLogger('backend.fastapi_app.process_analysis.economic_endpoint')

# Analytics imports
from analytics.economic.capex_analyzer import CapitalExpenditureAnalysis
from analytics.economic.opex_analyzer import OperationalExpenditureAnalysis, EmptyDataError
from analytics.economic.services.cost_tracking import CostTracker

# Model imports
from backend.fastapi_app.models.economic_analysis import (
    CapexInput, OpexInput, EconomicFactors, IndirectFactor,
    ComprehensiveAnalysisInput, BusinessMetricsResponse, ProcessType, UncertaintyConfig
)

# Service imports
from .services.profitability_service import ProfitabilityService
from .utils.error_handling import handle_analysis_error

# Initialize routers
capex_router = APIRouter(tags=["Capital Expenditure"])
opex_router = APIRouter(tags=["Operational Expenditure"])
profitability_router = APIRouter(tags=["Profitability Analysis"])

# Initialize services
profitability_service = ProfitabilityService()

#######################
# Utility Functions
#######################

def get_default_indirect_factors(equipment_cost: float) -> List[Dict[str, Any]]:
    """Get default indirect factors based on equipment cost"""
    return [
        {
            "name": "Engineering & Design",
            "cost": equipment_cost,
            "percentage": 0.15
        },
        {
            "name": "Construction Management",
            "cost": equipment_cost,
            "percentage": 0.20
        },
        {
            "name": "Contingency",
            "cost": equipment_cost,
            "percentage": 0.10  # Standard 10% contingency
        }
    ]

def validate_indirect_factor(factor: Dict[str, Any]) -> bool:
    """Validate a single indirect factor"""
    try:
        IndirectFactor(**factor)
        return True
    except Exception as e:
        logger.debug(f"Invalid indirect factor: {factor}. Error: {str(e)}")
        return False

#######################
# CAPEX Endpoints
#######################

@capex_router.post("/calculate")
async def calculate_capex(input_data: CapexInput) -> Dict[str, Any]:
    """Calculate total capital expenditure and its components"""
    try:
        logger.info(f"Received CAPEX calculation request for process type: {input_data.process_type}")
        
        # Initialize CAPEX analysis
        capex_analysis = CapitalExpenditureAnalysis()
        
        # Add equipment
        for equipment in input_data.equipment_list:
            # Add capacity-based cost adjustment and create equipment data
            equipment_data = {
                "name": equipment.name,
                "base_cost": equipment.base_cost,  # Use direct cost input
                "efficiency_factor": equipment.efficiency_factor,
                "installation_complexity": equipment.installation_complexity,
                "maintenance_cost": equipment.maintenance_cost,
                "energy_consumption": equipment.energy_consumption,
                "processing_capacity": equipment.processing_capacity
            }
            capex_analysis.add_equipment(equipment_data)
            
        logger.debug(f"Added {len(input_data.equipment_list)} equipment items")
        
        # Add indirect factors to the analyzer
        for factor in input_data.indirect_factors:
            capex_analysis.add_indirect_factor(factor.dict())
        logger.debug(f"Added {len(input_data.indirect_factors)} indirect factors")
        
        # Calculate total CAPEX
        capex_result = capex_analysis.calculate_total_capex(
            installation_factor=input_data.economic_factors.installation_factor,
            indirect_costs_factor=input_data.economic_factors.indirect_costs_factor
        )
        
        # Note: Working capital will be calculated in profitability service based on OPEX
        return {
            "capex_summary": {
                "total_capex": capex_result["total_capex"],
                "equipment_costs": capex_result["equipment_costs"],
                "installation_costs": capex_result["installation_costs"],
                "indirect_costs": capex_result["indirect_costs"],
                "total_investment": capex_result["total_investment"],
                "working_capital": 0.0
            },
            "equipment_breakdown": capex_result["equipment_breakdown"],
            "process_type": input_data.process_type,
            "production_volume": input_data.economic_factors.production_volume,
            "indirect_factors": {
                "source": "input",
                "factors": [factor.dict() for factor in input_data.indirect_factors]
            }
        }

    except ValueError as ve:
        logger.error(f"Validation error in CAPEX calculation: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in CAPEX calculation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@capex_router.get("/factors")
async def get_capex_factors() -> EconomicFactors:
    """Get default economic factors for CAPEX calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )

#######################
# OPEX Endpoints
#######################

@opex_router.post("/calculate")
async def calculate_opex(input_data: OpexInput) -> Dict[str, Any]:
    """Calculate total operational expenditure and its components"""
    try:
        logger.info(f"Received OPEX calculation request for process type: {input_data.process_type}")

        # Initialize OPEX analysis
        opex_analysis = OperationalExpenditureAnalysis()
        logger.debug("Initialized OperationalExpenditureAnalysis")

        # Set production volume first - this is required for scaling calculations
        production_volume = input_data.economic_factors.production_volume
        logger.debug(f"Setting production volume: {production_volume}")
        opex_analysis.set_production_volume(production_volume)

        # Add utilities with operating hours
        for utility in input_data.utilities:
            logger.debug(f"Processing utility: {utility.name}")
            utility_data = utility.model_dump()
            # Add operating hours if not present
            if "operating_hours" not in utility_data:
                utility_data["operating_hours"] = 8000  # Default to 8000 hours per year
            opex_analysis.add_utility(utility_data)

        # Add raw materials with protein content handling
        for material in input_data.raw_materials:
            logger.debug(f"Processing raw material: {material.name}")
            material_data = material.model_dump()
            # Handle protein content for pea flour
            if material.name.lower() == "pea flour":
                if hasattr(material, "protein_content") and material.protein_content is not None:
                    try:
                        protein_content = float(material.protein_content)
                        if 0 <= protein_content <= 1:  # Validate protein content is a valid percentage
                            material_data["protein_content"] = protein_content
                        else:
                            logger.warning(f"Invalid protein content range for pea flour: {protein_content}")
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid protein content value for pea flour: {material.protein_content}")
            material_data["protein_content"] = material.protein_content
            opex_analysis.add_raw_material(material_data)

        # Set labor data with benefits
        labor_config = input_data.labor_config.model_dump()
        if "benefits_factor" not in labor_config:
            labor_config["benefits_factor"] = 0.35  # Default 35% benefits
        logger.debug(f"Setting labor data with benefits factor: {labor_config['benefits_factor']}")
        opex_analysis.set_labor_data(labor_config)

        # Set maintenance factors
        maintenance_data = {
            "equipment_cost": input_data.equipment_costs,
            "maintenance_factor": input_data.economic_factors.maintenance_factor
        }
        logger.debug(f"Setting maintenance factors: {maintenance_data}")
        opex_analysis.set_maintenance_factors(maintenance_data)

        # Calculate total OPEX with scaling
        logger.debug("Calculating total OPEX with production scaling")
        opex_result = opex_analysis.calculate_total_opex()
        logger.debug("OPEX calculation completed")

        # Format response with detailed breakdowns
        return {
            "opex_summary": {
                "total_opex": opex_result["total_opex"],
                "cost_breakdown": opex_result["cost_breakdown"]
            },
            "detailed_breakdown": opex_result["detailed_breakdown"],
            "scaling_info": opex_result["scaling_info"],
            "process_type": input_data.process_type,
            "production_metrics": {
                "volume": production_volume,
                "operating_hours": 8000,  # Standard operating hours per year
                "capacity_utilization": opex_result["detailed_breakdown"]["labor"].get("staffing", {}).get("shifts", 1) / 3 * 100  # % of max capacity (3 shifts)
            }
        }

    except EmptyDataError as ede:
        logger.error(f"Missing required data in OPEX calculation: {str(ede)}")
        raise HTTPException(
            status_code=422,
            detail={"error": "Missing required data", "message": str(ede)}
        )
    except ValueError as ve:
        logger.error(f"Validation error in OPEX calculation: {str(ve)}")
        raise HTTPException(
            status_code=422,
            detail={"error": "Validation error", "message": str(ve)}
        )
    except Exception as e:
        logger.error(f"Error in OPEX calculation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "message": str(e)}
        )

@opex_router.get("/factors")
async def get_opex_factors() -> EconomicFactors:
    """Get default economic factors for OPEX calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0,
        maintenance_factor=0.05,
        installation_factor=0.2,  # Not used in OPEX but required by model
        indirect_costs_factor=0.15  # Not used in OPEX but required by model
    )

#######################
# Profitability Models
#######################

class SensitivityAnalysisInput(BaseModel):
    """Input model for sensitivity analysis"""
    base_cash_flows: List[float]
    variables: List[str] = ["discount_rate", "production_volume", "operating_costs", "revenue"]
    ranges: Dict[str, tuple] = {
        "discount_rate": (0.05, 0.15),
        "production_volume": (500.0, 1500.0),
        "operating_costs": (0.8, 1.2),
        "revenue": (0.8, 1.2)
    }
    steps: Optional[int] = 10
    fixed_cost_ratio: Optional[float] = None
    variable_cost_ratio: Optional[float] = None

class BusinessMetricsFilter(BaseModel):
    """Filter options for business metrics"""
    include_margins: bool = True
    include_break_even: bool = True
    include_cost_structure: bool = True
    include_efficiency: bool = True
    include_risk: bool = True

#######################
# Profitability Endpoints
#######################

async def get_cost_tracker():
    """Dependency injection for cost tracker"""
    return CostTracker()

@profitability_router.post("/analyze")
async def analyze_profitability(
    input_data: ComprehensiveAnalysisInput,
    cost_tracker: CostTracker = Depends(get_cost_tracker)
) -> Dict[str, Any]:
    """Perform comprehensive profitability analysis"""
    try:
        result = await profitability_service.analyze_comprehensive(input_data)
        
        # Track analysis in cost tracker
        cost_tracker.track_costs({
            "type": "profitability_analysis",
            "process_type": input_data.process_type,
            "timestamp": datetime.now().isoformat(),
            "metrics": result["profitability_metrics"],
            "business_insights": result["business_insights"]
        })
        
        return {
            "metrics": result["profitability_metrics"],
            "cash_flows": result["cash_flows"],
            "business_insights": result["business_insights"]
        }
    except Exception as e:
        return handle_analysis_error(e, "profitability analysis")

@profitability_router.post("/sensitivity")
async def analyze_sensitivity(input_data: SensitivityAnalysisInput) -> Dict[str, Any]:
    """Perform sensitivity analysis on economic metrics"""
    try:
        logger.debug(f"Starting sensitivity analysis with input: {input_data}")
        logger.debug(f"Base cash flows length: {len(input_data.base_cash_flows)}")
        logger.debug(f"Variables to analyze: {input_data.variables}")
        logger.debug(f"Ranges for variables: {input_data.ranges}")
        logger.debug(f"Number of steps: {input_data.steps}")
        
        result = await profitability_service.analyze_sensitivity(input_data)
        logger.debug(f"Sensitivity analysis result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in sensitivity analysis: {str(e)}", exc_info=True)
        return handle_analysis_error(e, "sensitivity analysis")

@profitability_router.get("/factors")
async def get_profitability_factors() -> EconomicFactors:
    """Get default economic factors for profitability calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0,
        installation_factor=0.3,
        indirect_costs_factor=0.45,
        maintenance_factor=0.02
    )

@profitability_router.get("/business-metrics")
async def get_business_metrics(
    filters: BusinessMetricsFilter = Depends(),
    cost_tracker: CostTracker = Depends(get_cost_tracker)
) -> BusinessMetricsResponse:
    """Get filtered business metrics and insights"""
    try:
        filtered_insights = {}
        
        # Apply filters
        if filters.include_margins:
            filtered_insights["profitability_indicators"] = {}
            
        if filters.include_break_even:
            filtered_insights["break_even_analysis"] = {}
            
        if filters.include_cost_structure:
            filtered_insights["cost_structure"] = {}
            
        if filters.include_efficiency:
            filtered_insights["cost_efficiency"] = {}
            
        if filters.include_risk:
            filtered_insights["risk_metrics"] = {}
            
        return BusinessMetricsResponse(
            timestamp=datetime.now().isoformat(),
            metrics=filtered_insights
        )
    except Exception as e:
        return handle_analysis_error(e, "business metrics retrieval")

@profitability_router.get("/performance-indicators")
async def get_performance_indicators(
    time_range: str = Query("1M", description="Time range for analysis (1M, 3M, 6M, 1Y)"),
    cost_tracker: CostTracker = Depends(get_cost_tracker)
) -> Dict[str, Any]:
    """Get key performance indicators and their trends over time"""
    try:
        return {
            "current_kpis": {},
            "historical_trends": {},
            "period_changes": {},
            "benchmarks": {}
        }
    except Exception as e:
        return handle_analysis_error(e, "performance indicators")

#######################
# Comprehensive Analysis
#######################

class UnifiedEconomicInput(BaseModel):
    """Unified input model for complete economic analysis"""
    process_type: ProcessType
    economic_factors: EconomicFactors
    equipment_list: List[Dict[str, Any]]
    indirect_factors: List[Dict[str, Any]]
    utilities: List[Dict[str, Any]]
    raw_materials: List[Dict[str, Any]]
    labor_config: Dict[str, Any]
    revenue_data: Dict[str, Any]
    analysis_config: Dict[str, Any]
    working_capital: Dict[str, Any] = {"inventory_months": 0, "receivables_days": 0, "payables_days": 0}  # Add with defaults

@profitability_router.post("/analyze/comprehensive")
async def analyze_comprehensive(
    input_data: UnifiedEconomicInput,
    cost_tracker: CostTracker = Depends(get_cost_tracker)
) -> Dict[str, Any]:
    """
    Perform comprehensive economic analysis including CAPEX, OPEX, profitability,
    sensitivity analysis, and business metrics in one request.
    """
    try:
        logger.info(f"Starting comprehensive analysis for process type: {input_data.process_type}")
        
        # Extract Monte Carlo config including random seed
        monte_carlo_config = input_data.analysis_config.get("monte_carlo", {})
        random_seed = monte_carlo_config.get("random_seed", 42)  # Default to 42 if not specified
        logger.debug(f"Using random seed: {random_seed}")
        
        # Calculate total equipment cost for default indirect factors if needed
        total_equipment_cost = sum(equip.get("base_cost", 0) for equip in input_data.equipment_list)
        
        # Use provided indirect factors or generate defaults
        indirect_factors = []
        if input_data.indirect_factors:
            # Convert dict factors to IndirectFactor models and ensure contingency is included
            has_contingency = False
            for factor in input_data.indirect_factors:
                try:
                    if factor.get("name", "").lower() == "contingency":
                        has_contingency = True
                    indirect_factors.append(IndirectFactor(**factor))
                except Exception as e:
                    logger.warning(f"Invalid indirect factor {factor}: {str(e)}")
            
            # Add default contingency if not provided
            if not has_contingency:
                contingency_cost = total_equipment_cost * 0.10  # 10% of equipment cost
                indirect_factors.append(IndirectFactor(
                    name="Contingency",
                    cost=contingency_cost,  # Add the required cost field
                    percentage=0.10,
                    reference_base="direct"
                ))
                logger.info("Added default contingency factor")
        
        if not indirect_factors:
            # Use defaults if no valid factors provided
            default_factors = get_default_indirect_factors(total_equipment_cost)
            indirect_factors = [IndirectFactor(**factor) for factor in default_factors]
            logger.info("Using default indirect factors")
        
        # 1. Prepare CAPEX input
        capex_input = CapexInput(
            equipment_list=input_data.equipment_list,
            indirect_factors=indirect_factors,
            economic_factors=input_data.economic_factors,
            process_type=input_data.process_type
        )
        
        # 2. Calculate CAPEX
        capex_results = await calculate_capex(capex_input)
        logger.debug("CAPEX analysis completed")
        
        # 3. Prepare OPEX input
        economic_factors_dict = input_data.economic_factors.dict()
        # Update production volume from revenue data if available
        economic_factors_dict["production_volume"] = input_data.revenue_data.get("annual_production", economic_factors_dict["production_volume"])
        
        # Define required fields for utilities
        required_fields = ["name", "consumption", "unit_price", "operating_hours", "unit"]

        # Format utilities with required fields
        formatted_utilities = []
        for utility in input_data.utilities:
            utility_data = utility.copy()  # Create a copy to modify
            logger.debug(f"Processing utility: {utility_data}")
            # Add operating hours if not present
            if "operating_hours" not in utility_data:
                utility_data["operating_hours"] = 8000  # Default to 8000 hours per year
                logger.debug("Added default operating hours")
            # Ensure all required fields are present
            if all(field in utility_data for field in required_fields):
                formatted_utilities.append(utility_data)
                logger.debug(f"Added valid utility: {utility_data}")
            else:
                missing_fields = [field for field in required_fields if field not in utility_data]
                logger.warning(f"Skipping utility due to missing fields {missing_fields}: {utility_data}")

        logger.debug(f"Final formatted utilities: {formatted_utilities}")

        if not formatted_utilities:
            raise ValueError("No valid utilities found after validation")
        
        opex_input = OpexInput(
            utilities=formatted_utilities,  # Use the formatted utilities list
            raw_materials=input_data.raw_materials,
            labor_config=input_data.labor_config,
            equipment_costs=capex_results["capex_summary"]["total_capex"],
            economic_factors=EconomicFactors(**economic_factors_dict),
            process_type=input_data.process_type
        )
        
        # 4. Calculate OPEX
        opex_results = await calculate_opex(opex_input)
        logger.debug("OPEX analysis completed")

        # Calculate working capital components
        annual_opex = opex_results["opex_summary"]["total_opex"]
        annual_revenue = input_data.revenue_data["product_price"] * input_data.revenue_data["annual_production"] * input_data.revenue_data.get("yield_efficiency", 1.0)
        
        # Inventory working capital (based on OPEX)
        inventory_months = input_data.working_capital.get("inventory_months", 2)
        inventory_wc = annual_opex * (inventory_months / 12)
        
        # Accounts receivable (based on revenue)
        receivables_days = input_data.working_capital.get("receivables_days", 30)
        receivables_wc = annual_revenue * (receivables_days / 365)
        
        # Accounts payable (based on OPEX)
        payables_days = input_data.working_capital.get("payables_days", 30)
        payables_wc = annual_opex * (payables_days / 365)
        
        # Total working capital
        working_capital = inventory_wc + receivables_wc - payables_wc
        logger.debug(f"Working capital components:")
        logger.debug(f"  Inventory ({inventory_months} months): ${inventory_wc:,.2f}")
        logger.debug(f"  Receivables ({receivables_days} days): ${receivables_wc:,.2f}")
        logger.debug(f"  Payables ({payables_days} days): ${payables_wc:,.2f}")
        logger.debug(f"Total working capital: ${working_capital:,.2f}")

        # Calculate total investment including working capital
        total_investment = (
            capex_results["capex_summary"]["total_investment"] +  # Use the CAPEX total investment
            working_capital
        )
        logger.debug(f"Total investment including working capital: {total_investment}")
        
        # Calculate updated investment efficiency metrics
        production_volume = input_data.revenue_data.get("annual_production", 0)
        if production_volume > 0:
            investment_per_unit = total_investment / production_volume
            revenue_to_investment = annual_revenue / total_investment if total_investment > 0 else 0.0
            opex_to_capex = annual_opex / capex_results["capex_summary"]["total_capex"] if capex_results["capex_summary"]["total_capex"] > 0 else 0.0
            logger.debug(f"Updated investment efficiency metrics:")
            logger.debug(f"  Investment per Unit: ${investment_per_unit:,.2f}")
            logger.debug(f"  Revenue to Investment: {revenue_to_investment:.2f}")
            logger.debug(f"  OPEX to CAPEX: {opex_to_capex:.2f}")
        
        # 5. Prepare profitability input
        profitability_input = ComprehensiveAnalysisInput(
            equipment_list=input_data.equipment_list,
            utilities=formatted_utilities,
            raw_materials=input_data.raw_materials,
            labor_config=input_data.labor_config,
            revenue_data=input_data.revenue_data,
            economic_factors=input_data.economic_factors,
            process_type=input_data.process_type,
            monte_carlo_iterations=monte_carlo_config.get("iterations", 1000),
            uncertainty=UncertaintyConfig(**monte_carlo_config.get("uncertainty", {})),
            random_seed=random_seed  # Pass the random seed
        )
        
        # 6. Calculate profitability
        profitability_results = await analyze_profitability(
            profitability_input,
            cost_tracker
        )
        logger.debug("Profitability analysis completed")
        logger.debug(f"Profitability results: {profitability_results}")
        
        # 7. Prepare and run sensitivity analysis if configured
        sensitivity_results = None
        if "sensitivity" in input_data.analysis_config:
            logger.info("=== Starting Sensitivity Analysis ===")
            logger.info(f"Sensitivity Config: {input_data.analysis_config['sensitivity']}")
            
            try:
                # Calculate fixed and variable costs from OPEX breakdown
                logger.info("\n=== Detailed Cost Breakdown Analysis ===")
                
                # Log OPEX breakdown details
                logger.info("OPEX Breakdown Details:")
                logger.info(f"Raw OPEX results: {opex_results}")
                logger.info(f"Cost breakdown: {opex_results['opex_summary']['cost_breakdown']}")
                
                # Calculate and log fixed costs components
                labor_costs = opex_results["opex_summary"]["cost_breakdown"]["labor"]
                maintenance_costs = opex_results["opex_summary"]["cost_breakdown"]["maintenance"]
                fixed_costs = labor_costs + maintenance_costs
                
                logger.info("\nFixed Costs Components:")
                logger.info(f"Labor Costs: ${labor_costs:,.2f}")
                logger.info(f"Maintenance Costs: ${maintenance_costs:,.2f}")
                logger.info(f"Total Fixed Costs: ${fixed_costs:,.2f}")
                
                # Calculate and log variable costs components
                raw_materials = opex_results["opex_summary"]["cost_breakdown"]["raw_materials"]
                utilities = opex_results["opex_summary"]["cost_breakdown"]["utilities"]
                variable_costs = raw_materials + utilities
                
                logger.info("\nVariable Costs Components:")
                logger.info(f"Raw Materials: ${raw_materials:,.2f}")
                logger.info(f"Utilities: ${utilities:,.2f}")
                logger.info(f"Total Variable Costs: ${variable_costs:,.2f}")
                
                # Calculate total costs and ratios
                total_costs = fixed_costs + variable_costs
                fixed_cost_ratio = fixed_costs / total_costs if total_costs > 0 else 0.0
                variable_cost_ratio = variable_costs / total_costs if total_costs > 0 else 0.0
                
                logger.info("\nCost Structure Summary:")
                logger.info(f"Total Costs: ${total_costs:,.2f}")
                logger.info(f"Fixed Cost Ratio: {fixed_cost_ratio:.4f} ({fixed_cost_ratio*100:.2f}%)")
                logger.info(f"Variable Cost Ratio: {variable_cost_ratio:.4f} ({variable_cost_ratio*100:.2f}%)")
                
                # Log values being passed to sensitivity analysis
                logger.info("\nSensitivity Analysis Input:")
                logger.info(f"Fixed Cost Ratio being passed: {fixed_cost_ratio:.4f}")
                logger.info(f"Variable Cost Ratio being passed: {variable_cost_ratio:.4f}")
                logger.info(f"Variables to analyze: {input_data.analysis_config['sensitivity']['variables']}")
                logger.info(f"Ranges: {input_data.analysis_config['sensitivity']['ranges']}")
                
                sensitivity_input = SensitivityAnalysisInput(
                    base_cash_flows=profitability_results["cash_flows"],
                    variables=input_data.analysis_config["sensitivity"]["variables"],
                    ranges=input_data.analysis_config["sensitivity"]["ranges"],
                    steps=input_data.analysis_config["sensitivity"]["steps"],
                    fixed_cost_ratio=fixed_cost_ratio,
                    variable_cost_ratio=variable_cost_ratio
                )
                logger.info(f"Cash flows for sensitivity: {profitability_results['cash_flows'][:5]}... (first 5 values)")
                logger.info(f"Number of cash flows: {len(profitability_results['cash_flows'])}")
                
                sensitivity_results = await analyze_sensitivity(sensitivity_input)
                logger.info("=== Sensitivity Analysis Results ===")
                for var, result in sensitivity_results['sensitivity_analysis'].items():
                    logger.info(f"Variable: {var}")
                    logger.info(f"Base NPV: ${result['base_npv']:,.2f}")
                    logger.info(f"Value range: [{result['range'][0]:,.2f}, {result['range'][-1]:,.2f}]")
                    logger.info("---")
                logger.info("=== Sensitivity Analysis Completed ===")
            except Exception as e:
                logger.error(f"Error during sensitivity analysis: {str(e)}", exc_info=True)
                raise
        else:
            logger.info("No sensitivity analysis configured in input_data.analysis_config")
        
        # 8. Get business metrics
        metrics_results = None
        if "metrics_filters" in input_data.analysis_config:
            filters = BusinessMetricsFilter(**input_data.analysis_config["metrics_filters"])
            metrics_results = await get_business_metrics(
                filters=filters,
                cost_tracker=cost_tracker
            )
            logger.debug("Business metrics analysis completed")
        
        # 9. Compile comprehensive results
        comprehensive_results = {
            "process_type": input_data.process_type,
            "timestamp": datetime.now().isoformat(),
            "capex_analysis": {
                "capex_summary": {
                    "total_capex": capex_results["capex_summary"]["total_capex"],
                    "equipment_costs": capex_results["capex_summary"]["equipment_costs"],
                    "installation_costs": capex_results["capex_summary"]["installation_costs"],
                    "indirect_costs": capex_results["capex_summary"]["indirect_costs"],
                    "working_capital": working_capital,
                    "total_investment": total_investment,
                    "base_investment": capex_results["capex_summary"]["total_investment"]  # Original CAPEX investment
                },
                "equipment_breakdown": capex_results["equipment_breakdown"],
                "indirect_factors": capex_results["indirect_factors"],
                "working_capital_components": {
                    "inventory": {
                        "value": inventory_wc,
                        "months": inventory_months
                    },
                    "receivables": {
                        "value": receivables_wc,
                        "days": receivables_days
                    },
                    "payables": {
                        "value": payables_wc,
                        "days": payables_days
                    }
                },
                "investment_efficiency": {
                    "per_unit": investment_per_unit if 'investment_per_unit' in locals() else 0.0,
                    "revenue_to_investment": revenue_to_investment if 'revenue_to_investment' in locals() else 0.0,
                    "opex_to_capex": opex_to_capex if 'opex_to_capex' in locals() else 0.0
                }
            },
            "opex_analysis": opex_results,
            "profitability_analysis": {
                "metrics": profitability_results["metrics"],
                "cash_flows": profitability_results["cash_flows"],
                "business_insights": profitability_results["business_insights"]
            },
            "sensitivity_analysis": sensitivity_results,
            "business_metrics": metrics_results,
            "financial_model": {
                "total_capex": capex_results["capex_summary"]["total_capex"],
                "working_capital": working_capital,
                "annual_net_cash_flows": profitability_results["cash_flows"][1:]
            }
        }
        
        if input_data.working_capital.get("inventory_months", 0) > 0:
            comprehensive_results["financial_model"]["initial_inventory"] = sum(
                rm["quantity"] * rm["unit_price"] * (input_data.working_capital["inventory_months"] / 12)
                for rm in input_data.raw_materials
            )
        
        logger.info(f"Comprehensive analysis completed for process type: {input_data.process_type}")
        return comprehensive_results
        
    except ValueError as ve:
        logger.error(f"Validation error in comprehensive analysis: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
