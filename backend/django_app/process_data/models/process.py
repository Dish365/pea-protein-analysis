from django.db import models
from enum import Enum
from process_data.validators import validate_equipment_structure

class ProcessType(str, Enum):
    BASELINE = 'baseline'
    RF = 'rf'
    IR = 'ir'
    
    @classmethod
    def choices(cls):
        return [(member.value, member.name) for member in cls]

class ProcessAnalysis(models.Model):
    PROCESS_TYPES = [
        (ProcessType.BASELINE.value, 'Baseline'),
        (ProcessType.RF.value, 'RF Treatment'),
        (ProcessType.IR.value, 'IR Treatment')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    # ===== Basic Info =====
    process_type = models.CharField(max_length=10, choices=PROCESS_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)
    
    # ===== Technical Analysis Inputs =====
    # Process Parameters
    air_flow = models.FloatField(help_text="Air flow rate in m³/h", default=0.0)
    classifier_speed = models.FloatField(help_text="Classifier wheel speed in rpm", default=0.0)
    
    # Mass Balance
    input_mass = models.FloatField(help_text="Input mass in kg", default=0.0)
    output_mass = models.FloatField(help_text="Output mass in kg", default=0.0)
    
    # Content Analysis
    initial_protein_content = models.FloatField(help_text="Initial protein content in %", default=0.0)
    final_protein_content = models.FloatField(help_text="Final protein content in %", default=0.0)
    initial_moisture_content = models.FloatField(help_text="Initial moisture content in %", default=0.0)
    final_moisture_content = models.FloatField(help_text="Final moisture content in %", default=0.0)
    
    # Particle Size Analysis
    d10_particle_size = models.FloatField(help_text="D10 particle size in μm", default=0.0)
    d50_particle_size = models.FloatField(help_text="D50 particle size in μm", default=0.0)
    d90_particle_size = models.FloatField(help_text="D90 particle size in μm", default=0.0)
    
    # ===== Economic Analysis Inputs =====
    # Equipment Configuration
    equipment = models.JSONField(
        help_text="List of equipment with details including base cost, efficiency factor, installation complexity",
        validators=[validate_equipment_structure],
        default=list
    )
    
    # Resource Configuration
    utilities = models.JSONField(
        help_text="List of utilities with consumption, unit price, unit",
        default=list
    )
    raw_materials = models.JSONField(
        help_text="List of raw materials with quantity, unit price, unit",
        default=list
    )
    labor_config = models.JSONField(
        help_text="Labor configuration with wages, hours, workers",
        default=dict
    )
    
    # Revenue Data
    revenue_data = models.JSONField(
        help_text="Revenue data including product price and annual production",
        default=dict
    )
    
    # Economic Factors
    economic_factors = models.JSONField(
        help_text="Economic factors including installation, indirect costs, maintenance factors, and project parameters",
        default=dict
    )
    
    # Analysis Parameters
    monte_carlo_iterations = models.IntegerField(
        help_text="Number of iterations for Monte Carlo simulation",
        default=1000
    )
    uncertainty = models.FloatField(
        help_text="Uncertainty factor for sensitivity analysis",
        default=0.1
    )
    
    # Financial Parameters
    project_duration = models.IntegerField(help_text="Project duration in years", default=1)
    discount_rate = models.FloatField(help_text="Discount rate in decimal", default=0.1)
    production_volume = models.FloatField(help_text="Annual production volume in kg", default=0.0)
    revenue_per_year = models.FloatField(help_text="Annual revenue in USD", default=0.0)
    cash_flows = models.JSONField(
        help_text="List of cash flows starting with initial investment",
        default=list
    )
    
    # Risk Analysis
    sensitivity_range = models.FloatField(default=0.2, help_text="Sensitivity analysis range")
    steps = models.IntegerField(default=10, help_text="Number of steps for sensitivity analysis")
    
    # ===== Environmental Analysis Inputs =====
    # Resource Consumption
    electricity_consumption = models.FloatField(help_text="Electricity consumption in kWh", default=0.0)
    cooling_consumption = models.FloatField(help_text="Cooling energy consumption in kWh", default=0.0)
    water_consumption = models.FloatField(help_text="Water consumption in kg", default=0.0)
    transport_consumption = models.FloatField(help_text="Transport energy consumption in MJ", default=0.0)
    equipment_mass = models.FloatField(help_text="Equipment mass in kg", default=0.0)
    thermal_ratio = models.FloatField(default=0.3, help_text="Thermal energy ratio")
    
    # Energy Data
    energy_consumption = models.JSONField(
        help_text="Detailed energy consumption breakdown",
        default=dict
    )
    
    # Production Data
    production_data = models.JSONField(
        help_text="Production data including mass flows and volume",
        default=dict
    )
    product_values = models.JSONField(
        help_text="Product value data including main and waste products",
        default=dict
    )
    
    # Allocation Configuration
    allocation_method = models.CharField(
        max_length=10,
        choices=[('economic', 'Economic'), ('physical', 'Physical'), ('hybrid', 'Hybrid')],
        default='hybrid',
        help_text="Method for impact allocation"
    )
    hybrid_weights = models.JSONField(
        help_text="Weights for hybrid allocation",
        default=dict
    )
    
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp']
        app_label = 'process_data'

def get_default_environmental_results():
    return {
        'impact_assessment': {
            'gwp': 0.0,
            'hct': 0.0,
            'frs': 0.0
        },
        'consumption_metrics': {
            'electricity': None,
            'cooling': None,
            'water': None
        }
    }

class AnalysisResult(models.Model):
    process = models.OneToOneField(ProcessAnalysis, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    technical_results = models.JSONField(
        null=True,
        help_text="Technical results including protein recovery, separation efficiency, process efficiency, particle size distribution",
        default=dict
    )
    economic_results = models.JSONField(
        null=True,
        help_text="Economic results including capex_analysis, opex_analysis, profitability_analysis",
        default=dict
    )
    environmental_results = models.JSONField(
        null=True,
        help_text="Environmental results including impact assessment and consumption metrics",
        default=get_default_environmental_results
    )
    efficiency_results = models.JSONField(
        null=True,
        help_text="Efficiency results including efficiency_metrics and performance_indicators",
        default=dict
    )
    
    class Meta:
        ordering = ['-timestamp'] 