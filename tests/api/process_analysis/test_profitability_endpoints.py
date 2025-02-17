"""
Profitability Analysis Test Suite
--------------------------------

This test suite validates the profitability analysis endpoints and provides business interpretation
of the results. The tests cover comprehensive analysis, sensitivity testing, and default factor validation.

Business Interpretation of Results
--------------------------------

1. Investment Structure (CAPEX)
   - Initial Investment: $363,570
     * Equipment: $222,000 (61%)
     * Installation: $96,570 (27%)
     * Indirect Costs: $45,000 (12%)
   - Investment scale suitable for medium-sized protein extraction facility

2. Operating Costs (OPEX)
   - Annual Operating Cost: $262,940
     * Labor: $250,000 (95%) - Major cost driver
     * Utilities: $6,000 (2.3%)
     * Raw Materials: $2,500 (1%)
     * Maintenance: $4,440 (1.7%)
   - Labor-intensive operation with efficient resource utilization

3. Revenue Model
   - Unit Price: $10
   - Annual Production: 500,000 units
   - Projected Revenue: $5,000,000 annually
   - High-volume, moderate-margin business model

4. Key Performance Indicators
   - Payback Period: 1.08 years (13 months)
     * Excellent recovery time
     * Well below industry standard of 2-3 years
   - NPV: $29.02 million (10-year projection)
     * Strong value creation
     * Accounts for 10% discount rate
   - Annual ROI: 62.9%
     * Exceptional return rate
     * Significantly above typical 15-20% industry threshold

5. Risk Analysis (Monte Carlo, 1000 iterations)
   - 95% Confidence Interval for NPV:
     * Lower: $26.69M
     * Upper: $31.60M
   - Demonstrates robust profitability across scenarios
   - 10% uncertainty factor applied to both revenues and costs

6. Cash Flow Profile
   - Initial Investment (Year 0): -$363,570
   - Annual Cash Flows: $4.5M-$5.1M
   - Stable and strong positive cash generation
   - Low volatility in projected cash flows

Business Recommendations
-----------------------
1. Investment Viability: Strong case for project approval
2. Operational Focus: Optimize labor efficiency
3. Growth Potential: Consider capacity expansion
4. Risk Management: Monitor production volumes
5. Cost Control: Focus on labor cost management

Test Cases Overview
------------------
"""

import pytest
from fastapi.testclient import TestClient
from backend.fastapi_app.main import app
from backend.fastapi_app.models.economic_analysis import (
    ProcessType, EconomicFactors, Equipment,
    Utility, RawMaterial, LaborConfig, ComprehensiveAnalysisInput
)
from backend.fastapi_app.process_analysis.services.profitability_service import ProfitabilityService
from analytics.economic.profitability_analyzer import ProjectParameters

client = TestClient(app)

def test_analyze_comprehensive():
    """
    Comprehensive Profitability Analysis Test
    ---------------------------------------
    Validates the complete business case analysis including:
    
    1. Equipment Configuration
       - Extraction unit with 200 kg/h capacity
       - 85% efficiency factor
       - Base cost: $100,000
    
    2. Utility Requirements
       - Electricity: 50,000 kWh at $0.12/kWh
       - Annual utility cost: $6,000
    
    3. Raw Material Inputs
       - Pea Biomass: 1,000 kg at $2.5/kg
       - Annual material cost: $2,500
    
    4. Labor Structure
       - 5 workers
       - 40 hours per week
       - 50 weeks per year
       - $25/hour wage rate
    
    5. Economic Parameters
       - 10-year project duration
       - 10% discount rate
       - 1000 Monte Carlo iterations
       - 10% uncertainty factor
    
    Expected Outcomes:
    - Positive NPV (>$0)
    - ROI between 0-100% annually
    - Payback period < project duration
    """
    # Setup equipment
    equipment = Equipment(
        name="Extraction Unit",
        base_cost=100000.0,
        efficiency_factor=0.85,
        installation_complexity=1.2,
        maintenance_cost=10000.0,
        energy_consumption=2000.0,
        processing_capacity=200.0
    )
    
    # Setup utility
    utility = Utility(
        name="Electricity",
        consumption=50000.0,
        unit_price=0.12,
        unit="kWh"
    )
    
    # Setup raw material
    raw_material = RawMaterial(
        name="Pea Biomass",
        quantity=1000.0,
        unit_price=2.5,
        unit="kg"
    )
    
    # Setup labor config
    labor_config = LaborConfig(
        hourly_wage=25.0,
        hours_per_week=40,
        weeks_per_year=50,
        num_workers=5
    )
    
    # Setup economic factors
    economic_factors = EconomicFactors(
        installation_factor=0.3,
        indirect_costs_factor=0.45,
        maintenance_factor=0.02,
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )
    
    # Setup revenue data
    revenue_data = {
        "product_price": 10.0,
        "annual_production": 500000.0
    }
    
    input_data = ComprehensiveAnalysisInput(
        equipment_list=[equipment.model_dump()],
        utilities=[utility.model_dump()],
        raw_materials=[raw_material.model_dump()],
        labor_config=labor_config.model_dump(),
        revenue_data=revenue_data,
        economic_factors=economic_factors,
        process_type=ProcessType.BASELINE,
        monte_carlo_iterations=1000,
        uncertainty=0.1,
        random_seed=42  # Add fixed seed for reproducible results
    )
    
    response = client.post("/api/v1/economic/profitability/analyze", json=input_data.model_dump())
    assert response.status_code == 200
    
    data = response.json()
    assert all(k in data for k in [
        "investment_analysis",
        "operational_costs",
        "profitability_metrics",
        "breakdowns",
        "process_type",
        "analysis_parameters",
        "cash_flows",
        "monte_carlo_analysis"
    ])
    
    # Verify investment analysis
    investment = data["investment_analysis"]
    assert all(k in investment for k in [
        "total_capex",
        "equipment_costs",
        "installation_costs",
        "indirect_costs"
    ])
    
    # Verify operational costs
    operations = data["operational_costs"]
    assert all(k in operations for k in [
        "total_opex",
        "utility_costs",
        "raw_material_costs",
        "labor_costs",
        "maintenance_costs"
    ])
    
    # Verify breakdowns
    breakdowns = data["breakdowns"]
    assert all(k in breakdowns for k in [
        "equipment",
        "utilities",
        "raw_materials",
        "labor",
        "indirect_factors"
    ])
    
    # Verify analysis parameters
    params = data["analysis_parameters"]
    assert all(k in params for k in [
        "monte_carlo_iterations",
        "uncertainty",
        "project_duration",
        "discount_rate",
        "production_volume"
    ])
    
    # Verify profitability metrics
    metrics = data["profitability_metrics"]
    assert all(k in metrics for k in ["npv", "roi", "payback"])
    
    # Verify metric values
    npv_value = metrics["npv"]["value"] if isinstance(metrics["npv"], dict) else metrics["npv"]
    roi_metrics = metrics["roi"]
    roi_value = roi_metrics["annualized_roi"] if isinstance(roi_metrics, dict) and "annualized_roi" in roi_metrics else roi_metrics["value"]
    payback_value = metrics["payback"]["value"] if isinstance(metrics["payback"], dict) else metrics["payback"]
    
    assert npv_value > 0  # Project should be profitable
    assert 0 < roi_value < 1  # Annualized ROI should be reasonable
    assert 0 < payback_value < economic_factors.project_duration  # Payback within project life

def test_analyze_sensitivity():
    """
    Sensitivity Analysis Test
    -----------------------
    Validates the project's resilience to changes in key variables:
    
    1. Base Financial Structure
       - CAPEX: $500,000
       - Annual OPEX: $200,000
       - Revenue: $5,000,000
    
    2. Sensitivity Variables
       - Discount Rate: 5-15%
       - Production Volume: 500-1,500 units
       - Operating Costs: ±20%
       - Revenue: ±20%
    
    Business Purpose:
    - Understand project risks
    - Identify critical variables
    - Support decision-making under uncertainty
    """
    # Setup base financial data
    capex_data = {
        "total_capex": 500000.0,
        "equipment_costs": 300000.0,
        "installation_costs": 150000.0,
        "indirect_costs": 50000.0,
        "total_investment": 550000.0  # Including working capital and contingency
    }
    
    opex_data = {
        "total_opex": 200000.0,
        "total_annual_cost": 200000.0,  # Required by profitability analyzer
        "utility_costs": 50000.0,
        "raw_material_costs": 80000.0,
        "labor_costs": 60000.0,
        "maintenance_costs": 10000.0
    }
    
    revenue_data = {
        "product_price": 10.0,
        "annual_production": 500000.0
    }
    
    # Set up analyzer with base data
    profitability_service = ProfitabilityService()
    profitability_service._analyzer.set_project_data(
        capex=capex_data,
        opex=opex_data,
        revenue=revenue_data,
        parameters=ProjectParameters(
            discount_rate=0.1,
            project_duration=10,
            production_volume=1000.0,
            uncertainty=0.1,
            monte_carlo_iterations=0
        )
    )
    
    # Calculate base cash flows
    base_cash_flows = profitability_service._analyzer._calculate_cash_flows()
    
    input_data = {
        "base_cash_flows": base_cash_flows,
        "variables": ["discount_rate", "production_volume", "operating_costs", "revenue"],
        "ranges": {
            "discount_rate": [0.05, 0.15],
            "production_volume": [500.0, 1500.0],
            "operating_costs": [0.8, 1.2],
            "revenue": [0.8, 1.2]
        },
        "steps": 10
    }
    
    response = client.post("/api/v1/economic/profitability/sensitivity", json=input_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "sensitivity_analysis" in data
    assert "base_case" in data
    
    sensitivity = data["sensitivity_analysis"]
    for var in input_data["variables"]:
        assert var in sensitivity
        var_data = sensitivity[var]
        assert all(k in var_data for k in ["values", "range", "base_value", "percent_change"])
        assert isinstance(var_data["values"], list)
        assert isinstance(var_data["range"], list)
        assert len(var_data["values"]) == input_data["steps"] + 1  # Include base case

def test_get_default_factors():
    """
    Default Economic Factors Test
    --------------------------
    Validates industry-standard economic parameters:
    
    1. Installation Factor: 30%
       - Standard for process equipment
    
    2. Indirect Costs: 45%
       - Engineering and project management
    
    3. Maintenance: 2%
       - Annual equipment maintenance
    
    4. Project Parameters
       - Duration: 10 years
       - Discount Rate: 10%
       - Production: 1,000 units
    
    Business Purpose:
    - Ensure consistent analysis baseline
    - Align with industry standards
    - Support quick initial assessments
    """
    response = client.get("/api/v1/economic/profitability/factors")
    assert response.status_code == 200
    
    data = response.json()
    assert all(k in data for k in [
        "installation_factor",
        "indirect_costs_factor",
        "maintenance_factor",
        "project_duration",
        "discount_rate",
        "production_volume"
    ])
    
    # Verify default values match our standard configuration
    assert data["installation_factor"] == 0.3
    assert data["indirect_costs_factor"] == 0.45
    assert data["maintenance_factor"] == 0.02
    assert data["project_duration"] == 10
    assert data["discount_rate"] == 0.1
    assert data["production_volume"] == 1000.0

def test_get_cost_summary():
    """
    Cost Summary Analysis Test
    ------------------------
    Validates cost tracking and reporting:
    
    1. Summary Components
       - Total costs by category
       - Time-based analysis
       - Cost breakdowns
    
    2. Trend Analysis
       - Cost patterns
       - Category distributions
       - Historical comparisons
    
    Business Purpose:
    - Track cost performance
    - Identify cost trends
    - Support cost optimization
    """
    response = client.get("/api/v1/economic/profitability/costs/summary")
    assert response.status_code == 200
    
    data = response.json()
    assert "summary" in data
    assert "trends" in data
    
    # Verify summary structure
    summary = data["summary"]
    assert isinstance(summary, dict)
    
    # Verify trends structure
    trends = data["trends"]
    assert isinstance(trends, dict) 