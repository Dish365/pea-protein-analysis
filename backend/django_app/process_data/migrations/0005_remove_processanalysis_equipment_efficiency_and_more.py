# Generated by Django 5.1.4 on 2025-01-21 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process_data', '0004_processanalysis_equipment_efficiency_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processanalysis',
            name='equipment_efficiency',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='hours_per_week',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='market_growth_rate',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='moisture_reduction',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='monte_carlo_iterations',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='num_workers',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='price_volatility',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='process_stages',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='revenue',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='selling_price',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='stage_efficiencies',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='target_protein_content',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='uncertainty',
        ),
        migrations.RemoveField(
            model_name='processanalysis',
            name='weeks_per_year',
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='allocation_method',
            field=models.CharField(choices=[('economic', 'Economic'), ('physical', 'Physical'), ('hybrid', 'Hybrid')], default='hybrid', help_text='Method for impact allocation', max_length=10),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='cash_flows',
            field=models.JSONField(default=list, help_text='List of cash flows starting with initial investment'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='energy_consumption',
            field=models.JSONField(default=dict, help_text='Detailed energy consumption breakdown'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='equipment',
            field=models.JSONField(default=list, help_text='List of equipment with details including cost, efficiency, maintenance'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='equipment_mass',
            field=models.FloatField(default=0.0, help_text='Equipment mass in kg'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='hybrid_weights',
            field=models.JSONField(default=dict, help_text='Weights for hybrid allocation'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='labor_config',
            field=models.JSONField(default=dict, help_text='Labor configuration with wages, hours, workers'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='product_values',
            field=models.JSONField(default=dict, help_text='Product value data including main and waste products'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='production_data',
            field=models.JSONField(default=dict, help_text='Production data including mass flows and volume'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='raw_materials',
            field=models.JSONField(default=list, help_text='List of raw materials with quantity, unit price, unit'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='revenue_per_year',
            field=models.FloatField(default=0.0, help_text='Annual revenue in USD'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='sensitivity_range',
            field=models.FloatField(default=0.2, help_text='Sensitivity analysis range'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='steps',
            field=models.IntegerField(default=10, help_text='Number of steps for sensitivity analysis'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='thermal_ratio',
            field=models.FloatField(default=0.3, help_text='Thermal energy ratio'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='transport_consumption',
            field=models.FloatField(default=0.0, help_text='Transport energy consumption in MJ'),
        ),
        migrations.AddField(
            model_name='processanalysis',
            name='utilities',
            field=models.JSONField(default=list, help_text='List of utilities with consumption, unit price, unit'),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='economic_results',
            field=models.JSONField(default=dict, help_text='Economic results including capex_analysis (summary, equipment_breakdown), opex_analysis (summary), profitability_analysis (metrics)', null=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='efficiency_results',
            field=models.JSONField(default=dict, help_text='Efficiency results including efficiency_metrics (economic, quality, resource) and performance_indicators', null=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='environmental_results',
            field=models.JSONField(default=dict, help_text='Environmental results including gwp, hct, frs, water_consumption', null=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='technical_results',
            field=models.JSONField(default=dict, help_text='Technical results including protein recovery, separation efficiency, process efficiency, particle size distribution', null=True),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='air_flow',
            field=models.FloatField(default=0.0, help_text='Air flow rate in m³/h'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='classifier_speed',
            field=models.FloatField(default=0.0, help_text='Classifier wheel speed in rpm'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='cooling_consumption',
            field=models.FloatField(default=0.0, help_text='Cooling energy consumption in kWh'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='d10_particle_size',
            field=models.FloatField(default=0.0, help_text='D10 particle size in μm'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='d50_particle_size',
            field=models.FloatField(default=0.0, help_text='D50 particle size in μm'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='d90_particle_size',
            field=models.FloatField(default=0.0, help_text='D90 particle size in μm'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='discount_rate',
            field=models.FloatField(default=0.1, help_text='Discount rate in decimal'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='electricity_consumption',
            field=models.FloatField(default=0.0, help_text='Electricity consumption in kWh'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='equipment_cost',
            field=models.FloatField(default=0.0, help_text='Base equipment cost in USD'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='final_moisture_content',
            field=models.FloatField(default=0.0, help_text='Final moisture content in %'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='final_protein_content',
            field=models.FloatField(default=0.0, help_text='Final protein content in %'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='indirect_factors',
            field=models.JSONField(default=list, help_text='List of indirect cost factors with name, cost, percentage'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='initial_moisture_content',
            field=models.FloatField(default=0.0, help_text='Initial moisture content in %'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='initial_protein_content',
            field=models.FloatField(default=0.0, help_text='Initial protein content in %'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='input_mass',
            field=models.FloatField(default=0.0, help_text='Input mass in kg'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='labor_cost',
            field=models.FloatField(default=0.0, help_text='Labor cost per hour in USD'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='maintenance_cost',
            field=models.FloatField(default=0.0, help_text='Annual maintenance cost in USD'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='output_mass',
            field=models.FloatField(default=0.0, help_text='Output mass in kg'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='production_volume',
            field=models.FloatField(default=0.0, help_text='Annual production volume in kg'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='project_duration',
            field=models.IntegerField(default=1, help_text='Project duration in years'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='raw_material_cost',
            field=models.FloatField(default=0.0, help_text='Raw material cost per kg in USD'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='utility_cost',
            field=models.FloatField(default=0.0, help_text='Utility cost per unit in USD'),
        ),
        migrations.AlterField(
            model_name='processanalysis',
            name='water_consumption',
            field=models.FloatField(default=0.0, help_text='Water consumption in kg'),
        ),
    ]
