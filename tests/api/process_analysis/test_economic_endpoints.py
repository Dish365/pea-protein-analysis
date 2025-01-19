import pytest
from typing import Dict, Any
from .conftest import ProcessAnalysisTester

class TestEconomicEndpoints:
    """Test suite for economic analysis endpoints"""
    
    @pytest.mark.asyncio
    async def test_capex_calculation(self, process_tester: ProcessAnalysisTester):
        """Test CAPEX calculation endpoint"""
        test_data = {
            'equipment_list': [
                {
                    'name': 'Centrifuge',
                    'cost': 50000.0,
                    'efficiency': 0.85,
                    'maintenance_cost': 2500.0,
                    'energy_consumption': 15.0,
                    'processing_capacity': 1000.0
                }
            ],
            'indirect_factors': [
                {
                    'name': 'Engineering',
                    'cost': 10000.0,
                    'percentage': 0.15
                }
            ],
            'installation_factor': 0.2,
            'indirect_costs_factor': 0.15
        }
        
        response = await process_tester.client.post(
            "/api/v1/economic/capex/calculate",
            json=test_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert 'capex_summary' in result
        assert 'equipment_breakdown' in result
        assert 'indirect_factors_breakdown' in result
        
        # Verify default factors
        factors_response = await process_tester.client.get(
            "/api/v1/economic/capex/factors"
        )
        assert factors_response.status_code == 200
        factors = factors_response.json()
        assert 'installation_factor' in factors
        assert 'indirect_costs_factor' in factors
        
    @pytest.mark.asyncio
    async def test_opex_calculation(self, process_tester: ProcessAnalysisTester):
        """Test OPEX calculation endpoint"""
        test_data = {
            'utilities': [
                {
                    'name': 'Electricity',
                    'consumption': 1000.0,
                    'unit_price': 0.12,
                    'unit': 'kWh'
                }
            ],
            'raw_materials': [
                {
                    'name': 'Peas',
                    'quantity': 5000.0,
                    'unit_price': 2.5,
                    'unit': 'kg'
                }
            ],
            'equipment_costs': 50000.0,
            'labor_config': {
                'hourly_wage': 25.0,
                'hours_per_week': 40,
                'weeks_per_year': 52,
                'num_workers': 2
            },
            'maintenance_factor': 0.05
        }
        
        response = await process_tester.client.post(
            "/api/v1/economic/opex/calculate",
            json=test_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert 'opex_summary' in result
        assert 'utilities_breakdown' in result
        assert 'raw_materials_breakdown' in result
        assert 'labor_breakdown' in result
        
        # Verify default factors
        factors_response = await process_tester.client.get(
            "/api/v1/economic/opex/factors"
        )
        assert factors_response.status_code == 200
        factors = factors_response.json()
        assert 'maintenance_factor' in factors
        
        # Verify the structure and values
        opex_summary = result['opex_summary']
        assert isinstance(opex_summary['total_opex'], (int, float))
        assert isinstance(opex_summary['raw_material_costs'], (int, float))
        assert isinstance(opex_summary['utility_costs'], (int, float))
        assert isinstance(opex_summary['labor_costs'], (int, float))
        assert isinstance(opex_summary['maintenance_costs'], (int, float))
        
        # Verify breakdowns
        assert len(result['utilities_breakdown']) == len(test_data['utilities'])
        assert len(result['raw_materials_breakdown']) == len(test_data['raw_materials'])
        
        # Verify labor breakdown
        labor_breakdown = result['labor_breakdown']
        assert isinstance(labor_breakdown['hourly_wage'], (int, float))
        assert isinstance(labor_breakdown['hours_per_week'], (int, float))
        assert isinstance(labor_breakdown['weeks_per_year'], (int, float))
        assert isinstance(labor_breakdown['num_workers'], (int, float))
        assert isinstance(labor_breakdown['annual_hours'], (int, float))
        assert isinstance(labor_breakdown['annual_cost_per_worker'], (int, float))
        
        # Verify labor breakdown values
        assert labor_breakdown['hourly_wage'] == test_data['labor_config']['hourly_wage']
        assert labor_breakdown['hours_per_week'] == test_data['labor_config']['hours_per_week']
        assert labor_breakdown['weeks_per_year'] == test_data['labor_config']['weeks_per_year']
        assert labor_breakdown['num_workers'] == test_data['labor_config']['num_workers']
        assert labor_breakdown['annual_hours'] == (
            test_data['labor_config']['hours_per_week'] * 
            test_data['labor_config']['weeks_per_year']
        )
        assert labor_breakdown['annual_cost_per_worker'] == (
            test_data['labor_config']['hourly_wage'] * 
            test_data['labor_config']['hours_per_week'] * 
            test_data['labor_config']['weeks_per_year']
        )
        
    @pytest.mark.asyncio
    async def test_monte_carlo_analysis(self, process_tester: ProcessAnalysisTester):
        """Test Monte Carlo profitability analysis endpoint"""
        test_data = {
            "cash_flows": [1000.0, 2000.0, 3000.0, 4000.0, 5000.0],
            "discount_rate": 0.1,
            "initial_investment": 10000.0,
            "gain_from_investment": 15000.0,
            "cost_of_investment": 10000.0,
            "production_volume": 1000.0,
            "monte_carlo_iterations": 1000,
            "uncertainty": 0.2
        }
        
        response = await process_tester.client.post(
            "/api/v1/economic/profitability/analyze",
            json=test_data
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "metrics" in data
        assert "monte_carlo" in data
        
        # Verify base metrics
        metrics = data["metrics"]
        assert "NPV" in metrics
        assert "ROI" in metrics
        assert "Payback Period" in metrics
        assert "Discounted Payback Period" in metrics
        assert "MCSP" in metrics
        assert "details" in metrics
        
        # Verify metric types
        assert isinstance(metrics["NPV"], (int, float))
        assert isinstance(metrics["ROI"], (int, float))
        assert isinstance(metrics["Payback Period"], (int, float))
        assert isinstance(metrics["Discounted Payback Period"], (int, float))
        assert isinstance(metrics["MCSP"], (int, float))
        
        # Verify Monte Carlo results
        monte_carlo = data["monte_carlo"]
        assert "iterations" in monte_carlo
        assert monte_carlo["iterations"] == test_data["monte_carlo_iterations"]
        assert "uncertainty" in monte_carlo
        assert monte_carlo["uncertainty"] == test_data["uncertainty"]
        assert "results" in monte_carlo
        
        # Verify Monte Carlo results structure
        results = monte_carlo["results"]
        assert "mean" in results
        assert "std_dev" in results
        assert "confidence_interval" in results
        assert isinstance(results["mean"], (int, float))
        assert isinstance(results["std_dev"], (int, float))
        assert isinstance(results["confidence_interval"], list)
        assert len(results["confidence_interval"]) == 2
        
    @pytest.mark.asyncio
    async def test_comprehensive_profitability(self, process_tester: ProcessAnalysisTester):
        """Test comprehensive profitability analysis endpoint"""
        test_data = {
            'capex': {
                'total_capex': 150000.0,
                'equipment_cost': 100000.0,
                'installation_cost': 20000.0,
                'indirect_cost': 30000.0
            },
            'opex': {
                'total_opex': 50000.0,
                'utilities_cost': 15000.0,
                'materials_cost': 20000.0,
                'labor_cost': 10000.0,
                'maintenance_cost': 5000.0
            },
            'production_volume': 10000.0,
            'project_duration': 10,
            'discount_rate': 0.1,
            'cash_flows': [-150000.0, 30000.0, 35000.0, 40000.0, 45000.0,
                          50000.0, 55000.0, 60000.0, 65000.0, 70000.0, 75000.0]
        }
        
        response = await process_tester.client.post(
            "/api/v1/economic/profitability",
            json=test_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # Verify investment analysis
        assert 'investment_analysis' in result
        investment = result['investment_analysis']
        assert 'direct_costs' in investment
        assert 'indirect_costs' in investment
        assert 'total_investment' in investment
        assert isinstance(investment['total_investment'], (int, float))
        
        # Verify annual costs
        assert 'annual_costs' in result
        costs = result['annual_costs']
        assert 'annual_capital_charge' in costs
        assert 'annual_opex' in costs
        assert 'total_annual_cost' in costs
        assert isinstance(costs['total_annual_cost'], (int, float))
        
        # Verify profitability metrics
        assert 'profitability_metrics' in result
        metrics = result['profitability_metrics']
        assert 'NPV' in metrics
        assert 'ROI' in metrics
        assert 'Payback Period' in metrics
        assert 'MCSP' in metrics
        assert isinstance(metrics['NPV'], (int, float))
        assert isinstance(metrics['ROI'], (int, float))
        assert isinstance(metrics['Payback Period'], (int, float, type(None)))
        
    @pytest.mark.asyncio
    async def test_sensitivity_analysis(self, process_tester: ProcessAnalysisTester):
        """Test sensitivity analysis endpoint"""
        test_data = {
            'base_cash_flows': [-150000.0, 30000.0, 35000.0, 40000.0, 45000.0],
            'discount_rate': 0.1,
            'production_volume': 10000.0,
            'sensitivity_range': 0.2,
            'steps': 10
        }
        
        response = await process_tester.client.post(
            "/api/v1/economic/profitability/sensitivity",
            json=test_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert 'sensitivity_analysis' in result
        
    @pytest.mark.asyncio
    async def test_cost_tracking(self, process_tester: ProcessAnalysisTester):
        """Test cost tracking endpoint"""
        response = await process_tester.client.get(
            "/api/v1/economic/cost-tracking"
        )
        
        assert response.status_code == 200
        result = response.json()
        assert 'cost_summary' in result
        assert 'cost_trends' in result