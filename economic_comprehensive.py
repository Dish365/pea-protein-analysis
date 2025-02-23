import requests
import json

 # Updated realistic payload for pea protein extraction process
payload = {
    "process_type": "baseline",
    "economic_factors": {
        "installation_factor": 0.35,      # Increased from 0.25 (more realistic for food processing)
        "indirect_costs_factor": 0.40,    # Increased from 0.35
        "maintenance_factor": 0.045,       # Increased from 0.03 (4.5% for hygienic equipment)
        "project_duration": 10,
        "discount_rate": 0.10,            # Increased from 0.08 (higher risk premium)
        "production_volume": 1500000
    },
    "equipment_list": [
        {
            "name": "Extraction Reactor",
            "base_cost": 1200000.0,       # Increased from 450k (realistic for sanitary design)
            "processing_capacity": 5000,
            "efficiency_factor": 0.78,     # Reduced from 0.88
            "installation_complexity": 1.35, # Increased from 1.25
            "maintenance_cost": 45000.0,  # Increased from 18k
            "energy_consumption": 180      # Increased from 150 kW
        },
        {
            "name": "Centrifugal Separator",
            "base_cost": 650000.0,        # Increased from 280k
            "processing_capacity": 2000,
            "efficiency_factor": 0.85,     # Reduced from 0.92
            "installation_complexity": 1.25,
            "maintenance_cost": 28000.0,  # Increased from 12k
            "energy_consumption": 110      # Increased from 90 kW
        }
    ],
    "indirect_factors": [
        {
            "name": "Engineering & Design",
            "cost": 275000.0,             # Increased from 175k
            "percentage": 0.15            # Increased from 0.12
        },
        {
            "name": "Construction Management",
            "cost": 325000.0,            # Increased from 225k
            "percentage": 0.20            # Increased from 0.18
        },
        {
            "name": "Contingency",
            "cost": 275000.0,  # Adding the required cost field
            "percentage": 0.15,           
            "reference_base": "direct"
        }
    ],
    "utilities": [
        {
            "name": "Steam",
            "consumption": 1500,          # Increased from 1200 kg/h
            "unit_price": 0.028,          # Increased from 0.025
            "operating_hours": 6000,
            "unit": "kg"
        },
        {
            "name": "Electricity",
            "consumption": 950,           # Increased from 850 kW
            "unit_price": 0.105,          # Increased from 0.095
            "operating_hours": 8000,
            "unit": "kWh"
        }
    ],
    "raw_materials": [
        {
            "name": "Pea Flour",
            "quantity": 2500000.0,
            "unit_price": 0.92,           # Increased from 0.85 (current market)
            "protein_content": 0.25,
            "unit": "kg"
        },
        {
            "name": "NaOH",
            "quantity": 15000.0,
            "unit_price": 0.35,           # Reduced from 0.45 (bulk pricing)
            "unit": "kg"
        }
    ],
    "labor_config": {
        "hourly_wage": 35.75,             # Increased from 32.50
        "hours_per_week": 40,
        "weeks_per_year": 52,
        "num_workers": 15,                # Increased from 12
        "benefits_factor": 0.30           # Reduced from 0.35
    },
    "revenue_data": {
        "product_price": 6.50,            # Reduced from 7.50 (competitive pricing)
        "annual_production": 1500000,
        "yield_efficiency": 0.70          # Reduced from 0.78
    },
    "analysis_config": {
        "monte_carlo": {
            "iterations": 10000,          # Increased from 5000
            "uncertainty": {
                "price": 0.30,            # Increased from 0.25
                "cost": 0.25              # Increased from 0.20
            },
            "random_seed": 42             # Add fixed seed for reproducible results
        },
        "sensitivity": {
            "variables": ["product_price", "pea_flour_cost", "energy_costs"],
            "ranges": {
                "product_price": [5.00, 8.00],  # Wider range
                "pea_flour_cost": [0.75, 1.25], # Increased volatility
                "energy_costs": [0.085, 0.125]
            },
            "steps": 15
        },
        "metrics_filters": {
            "include_margins": True,
            "include_break_even": True,
            "include_cost_structure": True,
            "include_efficiency": True,
            "include_risk": True
        }
    },
    "working_capital": {
        "inventory_months": 3,
        "receivables_days": 45,
        "payables_days": 30
    }
}

# Make the request
response = requests.post(
    "http://localhost:8001/api/v1/economic/profitability/analyze/comprehensive",
    json=payload
)

# Handle the response
if response.status_code == 200:
    results = response.json()
    print("\n=== Comprehensive Economic Analysis Results ===\n")
    
    # CAPEX and OPEX Summary
    print("Capital and Operational Expenditure:")
    capex_summary = results.get('capex_analysis', {}).get('capex_summary', {})
    print(f"Base CAPEX: ${capex_summary.get('total_capex', 0):,.2f}")
    
    # Working Capital Breakdown
    print("\nWorking Capital Components:")
    wc_components = results.get('capex_analysis', {}).get('working_capital_components', {})
    inventory = wc_components.get('inventory', {})
    receivables = wc_components.get('receivables', {})
    payables = wc_components.get('payables', {})
    
    print(f"Inventory ({inventory.get('months', 0)} months): ${inventory.get('value', 0):,.2f}")
    print(f"Accounts Receivable ({receivables.get('days', 0)} days): ${receivables.get('value', 0):,.2f}")
    print(f"Accounts Payable ({payables.get('days', 0)} days): ${payables.get('value', 0):,.2f}")
    print(f"Net Working Capital: ${capex_summary.get('working_capital', 0):,.2f}")
    
    print(f"\nTotal Investment: ${capex_summary.get('total_investment', 0):,.2f}")
    print(f"Annual OPEX: ${results.get('opex_analysis', {}).get('opex_summary', {}).get('total_opex', 0):,.2f}")
    
    # Core Profitability Metrics
    print("\nCore Profitability Metrics:")
    metrics = results['profitability_analysis']['metrics']

    # Get NPV either directly or from monte_carlo results
    npv = metrics.get('npv', {}).get('value')
    if npv is None and 'monte_carlo' in metrics and 'results' in metrics['monte_carlo']:
        npv = metrics['monte_carlo']['results'].get('mean')
    print(f"NPV: ${npv:,.2f}" if npv is not None else "NPV: Not available")

    # Get ROI
    roi = metrics.get('roi', {}).get('value', 0) * 100
    print(f"ROI: {roi:.1f}%")

    # Get Payback Period
    payback = metrics.get('payback', {}).get('value', 'N/A')
    print(f"Payback Period: {payback:.1f} years" if isinstance(payback, (int, float)) else "Payback Period: N/A")

    # Margins
    print("\nMargins:")
    margins = metrics.get('margins', {})
    gross_margin = margins.get('gross_margin', {}).get('value', 0) * 100
    operating_margin = margins.get('operating_margin', {}).get('value', 0) * 100
    print(f"Gross Margin: {gross_margin:.1f}%")
    print(f"Operating Margin: {operating_margin:.1f}%")

    # Cost Structure
    print("\nCost Structure:")
    cost_structure = metrics.get('cost_structure', {})
    fixed_costs = cost_structure.get('fixed_costs', {})
    variable_costs = cost_structure.get('variable_costs', {})

    if fixed_costs and variable_costs:
        print(f"Fixed Costs: ${fixed_costs.get('value', 0):,.2f} ({fixed_costs.get('percentage', 0):.1f}%)")
        print(f"Variable Costs: ${variable_costs.get('value', 0):,.2f} ({variable_costs.get('percentage', 0):.1f}%)")
        
        # Detailed Cost Breakdown
        print("\nDetailed Cost Breakdown:")
        fixed_breakdown = fixed_costs.get('breakdown', {})
        variable_breakdown = variable_costs.get('breakdown', {})
        print(f"  Labor: ${fixed_breakdown.get('labor', 0):,.2f}")
        print(f"  Maintenance: ${fixed_breakdown.get('maintenance', 0):,.2f}")
        print(f"  Raw Materials: ${variable_breakdown.get('raw_materials', 0):,.2f}")
        print(f"  Utilities: ${variable_breakdown.get('utilities', 0):,.2f}")
    else:
        print("Cost structure not available")

    # Investment Efficiency
    print("\nInvestment Efficiency:")
    efficiency = results.get('capex_analysis', {}).get('investment_efficiency', {})
    print(f"Investment per Unit: ${efficiency.get('per_unit', 0):,.2f}")
    print(f"Revenue to Investment Ratio: {efficiency.get('revenue_to_investment', 0):.2f}")
    print(f"OPEX to CAPEX Ratio: {efficiency.get('opex_to_capex', 0):.2f}")

    # Annual Performance
    print("\nAnnual Performance:")
    annual = metrics.get('annual_metrics', {})
    if not annual:  # If annual_metrics not present, try to get from financial_model
        financial_model = results.get('financial_model', {})
        annual = {
            'revenue': financial_model.get('annual_revenue', 0),
            'operating_costs': financial_model.get('annual_operating_costs', 0),
            'total_costs': financial_model.get('total_annual_costs', 0)
        }
    print(f"Revenue: ${annual.get('revenue', 0):,.2f}")
    print(f"Operating Costs: ${annual.get('operating_costs', 0):,.2f}")
    print(f"Total Costs: ${annual.get('total_costs', 0):,.2f}")

    # Break-even Analysis
    print("\nBreak-even Analysis:")
    breakeven = metrics.get('break_even', {})
    def format_break_even(value):
        if value == float('inf'):
            return "N/A (Not Achievable)"
        return f"{value:,.0f}" if isinstance(value, (int, float)) else "N/A"

    print(f"Break-even Units: {format_break_even(breakeven.get('units', 0))}")
    print(f"Break-even Revenue: ${format_break_even(breakeven.get('revenue', 0))}")

    # Monte Carlo Analysis
    if 'monte_carlo' in metrics and 'results' in metrics['monte_carlo']:
        mc = metrics['monte_carlo']
        print("\nMonte Carlo Analysis:")
        print(f"Mean NPV: ${mc['results'].get('mean', 0):,.2f}")
        print(f"Standard Deviation: ${mc['results'].get('std_dev', 0):,.2f}")
        ci = mc['results'].get('confidence_interval', [0, 0])
        if isinstance(ci, list) and len(ci) == 2:
            print(f"95% Confidence Interval: ${ci[0]:,.2f} to ${ci[1]:,.2f}")
        elif isinstance(ci, dict):
            print(f"95% Confidence Interval: ${ci.get('lower', 0):,.2f} to ${ci.get('upper', 0):,.2f}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
