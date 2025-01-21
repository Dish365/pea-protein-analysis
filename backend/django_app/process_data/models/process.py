from django.db import models
from enum import Enum

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
    
    # ===== Shared Process Inputs =====
    # Basic Info
    process_type = models.CharField(max_length=10, choices=PROCESS_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)
    
    # Process Parameters
    air_flow = models.FloatField(help_text="Air flow rate in m³/h")
    classifier_speed = models.FloatField(help_text="Classifier wheel speed in rpm")
    production_volume = models.FloatField(help_text="Annual production volume in kg")
    
    # Operating Schedule
    hours_per_week = models.IntegerField(
        default=40,
        help_text="Working hours per week"
    )
    weeks_per_year = models.IntegerField(
        default=52,
        help_text="Working weeks per year"
    )
    num_workers = models.IntegerField(
        default=1,
        help_text="Number of workers"
    )
    
    # ===== Technical Analysis Inputs =====
    # Mass Balance
    input_mass = models.FloatField(help_text="Input mass in kg")
    output_mass = models.FloatField(help_text="Output mass in kg")
    
    # Protein Content
    initial_protein_content = models.FloatField(help_text="Initial protein content in %")
    final_protein_content = models.FloatField(help_text="Final protein content in %")
    target_protein_content = models.FloatField(null=True, blank=True, help_text="Target protein content in %")
    
    # Moisture Content
    initial_moisture_content = models.FloatField(help_text="Initial moisture content in %")
    final_moisture_content = models.FloatField(help_text="Final moisture content in %")
    moisture_reduction = models.FloatField(help_text="Moisture reduction achieved in %", null=True)
    
    # Particle Size Analysis
    d10_particle_size = models.FloatField(help_text="D10 particle size in μm")
    d50_particle_size = models.FloatField(help_text="D50 particle size in μm")
    d90_particle_size = models.FloatField(help_text="D90 particle size in μm")
    particle_size_span = models.FloatField(help_text="Particle size distribution span", null=True)
    particle_size_cv = models.FloatField(help_text="Coefficient of variation for particle size", null=True)
    particle_density = models.FloatField(default=1.5, help_text="Particle density in g/cm³")
    
    # Technical Performance Metrics
    protein_recovery = models.FloatField(null=True, help_text="Protein recovery rate in %")
    separation_efficiency = models.FloatField(null=True, help_text="Overall separation efficiency in %")
    protein_enrichment = models.FloatField(null=True, help_text="Absolute protein enrichment in %")
    separation_factor = models.FloatField(null=True, help_text="Protein/non-protein separation factor")
    component_recoveries = models.JSONField(null=True, help_text="Recovery rates for each component")
    
    # Multi-stage Process Data
    process_stages = models.JSONField(null=True, blank=True, help_text="Data for each process stage")
    stage_efficiencies = models.JSONField(null=True, blank=True, help_text="Efficiency metrics for each stage")
    cumulative_efficiency = models.FloatField(null=True, help_text="Cumulative process efficiency in %")
    average_step_efficiency = models.FloatField(null=True, help_text="Average efficiency across stages in %")
    purity_achievement = models.FloatField(null=True, help_text="Progress toward target purity in %")
    stage_contributions = models.JSONField(null=True, help_text="Contribution analysis for each stage")
    
    # ===== Economic Analysis Inputs =====
    # Capital Costs
    equipment_cost = models.FloatField(help_text="Equipment cost in USD")
    installation_factor = models.FloatField(default=0.2, help_text="Installation cost factor")
    indirect_costs_factor = models.FloatField(default=0.15, help_text="Indirect costs factor")
    indirect_factors = models.JSONField(null=True, blank=True, help_text="List of indirect cost factors with name, cost, and percentage values")
    
    # Operating Costs
    maintenance_cost = models.FloatField(help_text="Annual maintenance cost in USD")
    maintenance_factor = models.FloatField(default=0.05, help_text="Maintenance cost factor")
    raw_material_cost = models.FloatField(help_text="Raw material cost per kg in USD")
    utility_cost = models.FloatField(help_text="Utility cost per kWh in USD")
    labor_cost = models.FloatField(help_text="Labor cost per hour in USD")
    
    # Financial Parameters
    project_duration = models.IntegerField(help_text="Project duration in years")
    discount_rate = models.FloatField(help_text="Discount rate in decimal")
    selling_price = models.FloatField(null=True, blank=True, help_text="Product selling price per kg in USD")
    market_growth_rate = models.FloatField(null=True, blank=True, help_text="Expected market growth rate")
    price_volatility = models.FloatField(null=True, blank=True, help_text="Price volatility factor")
    revenue = models.JSONField(null=True, blank=True, help_text="Annual revenue projections")
    
    # Risk Analysis
    monte_carlo_iterations = models.IntegerField(default=1000, help_text="Number of Monte Carlo simulation iterations")
    uncertainty = models.FloatField(default=0.1, help_text="Uncertainty factor for Monte Carlo simulation")
    
    # Equipment Performance
    equipment_efficiency = models.FloatField(
        default=0.85,
        help_text="Equipment efficiency factor (0-1)"
    )
    
    # ===== Environmental Analysis Inputs =====
    # Resource Consumption
    electricity_consumption = models.FloatField(help_text="Electricity consumption in kWh")
    cooling_consumption = models.FloatField(help_text="Cooling energy consumption in kWh")
    water_consumption = models.FloatField(help_text="Water consumption in kg")
    
    class Meta:
        ordering = ['-timestamp']

class AnalysisResult(models.Model):
    process = models.OneToOneField(ProcessAnalysis, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Results as JSON fields
    technical_results = models.JSONField(null=True)
    economic_results = models.JSONField(null=True)
    environmental_results = models.JSONField(null=True)
    efficiency_results = models.JSONField(null=True)
    
    class Meta:
        ordering = ['-timestamp'] 