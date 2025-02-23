import pytest
from datetime import datetime
from analytics.pipeline.integrator.economic import EconomicIntegrator

@pytest.fixture
def process_data():
    """Real process data for integration testing"""
    return {
        'equipment': [{
            'name': 'Extraction Unit',
            'base_cost': 100000.0,
            'efficiency_factor': 0.85,
            'installation_complexity': 1.2,
            'maintenance_cost': 10000.0,
            'energy_consumption': 2000.0,
            'processing_capacity': 200.0
        }],
        'utilities': [{
            'name': 'Electricity',
            'consumption': 50000.0,
            'unit_price': 0.12,
            'unit': 'kWh'
        }],
        'raw_materials': [{
            'name': 'Pea Biomass',
            'quantity': 1000.0,
            'unit_price': 2.5,
            'unit': 'kg'
        }],
        'labor_config': {
            'hourly_wage': 25.0,
            'hours_per_week': 40,
            'weeks_per_year': 50,
            'num_workers': 5
        },
        'revenue_data': {
            'product_price': 10.0,
            'annual_production': 500000.0
        },
        'economic_factors': {
            'installation_factor': 0.3,
            'indirect_costs_factor': 0.45,
            'maintenance_factor': 0.02,
            'project_duration': 10,
            'discount_rate': 0.1,
            'production_volume': 1000.0
        },
        'process_type': 'baseline',
        'monte_carlo_iterations': 1000,
        'uncertainty': 0.1,
        'equipment_costs': 222000.0  # Added equipment costs from successful CAPEX calculation
    }

@pytest.mark.asyncio
async def test_economic_analysis_integration(process_data):
    """
    Integration test for the complete economic analysis pipeline.
    Tests actual endpoint orchestration with real API calls.
    
    This test requires:
    1. FastAPI server running at http://localhost:8001
    2. All economic analysis endpoints functional
    3. Network connectivity to the server
    """
    async with EconomicIntegrator() as integrator:
        # Perform complete economic analysis
        result = await integrator.analyze_economics(process_data)
        
        # 1. Verify CAPEX Analysis
        capex = result['capex_analysis']
        assert capex['summary']['total_capex'] > 0, "Total CAPEX should be positive"
        assert capex['summary']['equipment_costs'] > 0, "Equipment costs should be positive"
        assert capex['summary']['installation_costs'] > 0, "Installation costs should be positive"
        assert capex['summary']['indirect_costs'] > 0, "Indirect costs should be positive"
        
        assert len(capex['equipment_breakdown']) == 1, "Should have one equipment item"
        equipment = capex['equipment_breakdown'][0]
        assert equipment['name'] == process_data['equipment'][0]['name']
        assert equipment['base_cost'] == process_data['equipment'][0]['base_cost']
        assert capex['process_type'] == process_data['process_type']
        
        # 2. Verify OPEX Analysis
        opex = result['opex_analysis']
        assert opex['summary']['total_opex'] > 0, "Total OPEX should be positive"
        assert opex['summary']['utility_costs'] > 0, "Utility costs should be positive"
        assert opex['summary']['raw_material_costs'] > 0, "Material costs should be positive"
        assert opex['summary']['labor_costs'] > 0, "Labor costs should be positive"
        assert opex['summary']['maintenance_costs'] > 0, "Maintenance costs should be positive"
        
        # Verify OPEX breakdowns match input data
        utilities = opex['utilities_breakdown']
        assert len(utilities) == len(process_data['utilities'])
        assert utilities[0]['name'] == process_data['utilities'][0]['name']
        assert utilities[0]['consumption'] == process_data['utilities'][0]['consumption']
        
        materials = opex['raw_materials_breakdown']
        assert len(materials) == len(process_data['raw_materials'])
        assert materials[0]['name'] == process_data['raw_materials'][0]['name']
        assert materials[0]['quantity'] == process_data['raw_materials'][0]['quantity']
        
        labor = opex['labor_breakdown']
        assert labor['hourly_wage'] == process_data['labor_config']['hourly_wage']
        assert labor['hours_per_week'] == process_data['labor_config']['hours_per_week']
        assert labor['num_workers'] == process_data['labor_config']['num_workers']
        
        # 3. Verify Profitability Analysis
        profitability = result['profitability_analysis']
        metrics = profitability['metrics']
        
        # Verify NPV
        assert 'npv' in metrics
        assert isinstance(metrics['npv']['value'], (int, float))
        assert metrics['npv']['unit'] == 'USD'
        
        # Verify ROI
        assert 'roi' in metrics
        assert isinstance(metrics['roi']['value'], (int, float))
        assert metrics['roi']['unit'] == 'ratio'
        
        # Verify Payback
        assert 'payback' in metrics
        assert isinstance(metrics['payback']['value'], (int, float))
        assert metrics['payback']['unit'] == 'years'
        
        # Verify cash flows
        cash_flows = profitability['cash_flows']
        assert len(cash_flows) == process_data['economic_factors']['project_duration'] + 1
        assert cash_flows[0] < 0, "Initial investment should be negative"
        assert all(cf > 0 for cf in cash_flows[1:]), "Annual cash flows should be positive"
        
        # Verify Monte Carlo results
        monte_carlo = profitability.get('monte_carlo')
        if monte_carlo:
            assert monte_carlo['iterations'] == process_data['monte_carlo_iterations']
            assert 'results' in monte_carlo
            results = monte_carlo['results']
            assert 'mean' in results
            assert 'std_dev' in results
            assert 'confidence_interval' in results
        
        # 4. Verify Sensitivity Analysis
        sensitivity = result['sensitivity_analysis']
        expected_variables = ['discount_rate', 'production_volume', 'operating_costs', 'revenue']
        for var in expected_variables:
            assert var in sensitivity, f"Should have sensitivity analysis for {var}"
            var_results = sensitivity[var]
            assert 'values' in var_results
            assert 'range' in var_results
            assert 'base_value' in var_results
            assert 'percent_change' in var_results
            
            # Verify ranges match input
            if var == 'production_volume':
                values = var_results['range']
                expected_min = process_data['economic_factors']['production_volume'] * 0.5
                expected_max = process_data['economic_factors']['production_volume'] * 1.5
                assert values[0] == expected_min, "Range should start at expected minimum"
                assert values[-1] == expected_max, "Range should end at expected maximum"
                assert len(values) == 11, "Should have 11 points (10 steps + endpoints)"
                assert all(values[i] < values[i+1] for i in range(len(values)-1)), "Values should be strictly increasing"
        
        # 5. Verify Metadata
        metadata = result['metadata']
        assert metadata['process_type'] == process_data['process_type']
        assert 'timestamp' in metadata
        
        # Verify data sources
        data_sources = metadata['data_sources']
        assert all(data_sources[source] for source in ['capex', 'opex', 'profitability', 'sensitivity'])
        
        # Verify analysis parameters
        analysis_params = metadata['analysis_parameters']
        assert analysis_params['project_duration'] == process_data['economic_factors']['project_duration']
        assert analysis_params['discount_rate'] == process_data['economic_factors']['discount_rate']
        assert analysis_params['monte_carlo_iterations'] == process_data['monte_carlo_iterations']
        assert analysis_params['uncertainty'] == process_data['uncertainty']
        