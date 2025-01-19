from django.db import models
from django.core.exceptions import ValidationError
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
    
    # Basic Info
    process_type = models.CharField(max_length=10, choices=PROCESS_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Technical Parameters
    input_mass = models.FloatField(help_text="Input mass in kg")
    output_mass = models.FloatField(help_text="Output mass in kg")
    initial_protein_content = models.FloatField(help_text="Initial protein content in %")
    final_protein_content = models.FloatField(help_text="Final protein content in %")
    initial_moisture_content = models.FloatField(help_text="Initial moisture content in %")
    final_moisture_content = models.FloatField(help_text="Final moisture content in %")
    moisture_reduction = models.FloatField(help_text="Moisture reduction achieved in %", null=True)
    d10_particle_size = models.FloatField(help_text="D10 particle size in μm")
    d50_particle_size = models.FloatField(help_text="D50 particle size in μm")
    d90_particle_size = models.FloatField(help_text="D90 particle size in μm")
    
    # Economic Parameters
    equipment_cost = models.FloatField(help_text="Equipment cost in USD")
    maintenance_cost = models.FloatField(help_text="Annual maintenance cost in USD")
    raw_material_cost = models.FloatField(help_text="Raw material cost per kg in USD")
    utility_cost = models.FloatField(help_text="Utility cost per hour in USD")
    labor_cost = models.FloatField(help_text="Labor cost per hour in USD")
    project_duration = models.IntegerField(help_text="Project duration in years")
    discount_rate = models.FloatField(help_text="Discount rate in decimal")
    production_volume = models.FloatField(help_text="Annual production volume in kg")
    
    # Environmental Parameters
    electricity_consumption = models.FloatField(help_text="Electricity consumption in kWh")
    cooling_consumption = models.FloatField(help_text="Cooling energy consumption in kWh")
    water_consumption = models.FloatField(help_text="Water consumption in kg")
    
    class Meta:
        ordering = ['-timestamp']
        
    def clean(self):
        """Validate process-specific constraints"""
        super().clean()
        
        # Process type validation
        if self.process_type not in [pt.value for pt in ProcessType]:
            raise ValidationError(f"Invalid process type. Must be one of: {', '.join([pt.value for pt in ProcessType])}")
        
        # Process-specific validations
        if self.process_type == ProcessType.RF.value:
            if self.electricity_consumption <= 0:
                raise ValidationError("RF treatment requires positive electricity consumption")
            if self.initial_moisture_content < 13.6:
                raise ValidationError("RF treatment requires ≥13.6% initial moisture content")
        elif self.process_type == ProcessType.IR.value:
            if self.cooling_consumption <= 0:
                raise ValidationError("IR treatment requires positive cooling consumption")
            if abs(self.initial_moisture_content - 15.5) > 0.5:
                raise ValidationError("IR treatment requires ~15.5% initial moisture content")
        
        # Mass balance validation
        if self.output_mass > self.input_mass:
            raise ValidationError("Output mass cannot exceed input mass")
        if self.input_mass <= 0 or self.output_mass <= 0:
            raise ValidationError("Input and output mass must be positive")
            
        # Content range validations
        if not (0 <= self.initial_protein_content <= 100):
            raise ValidationError("Initial protein content must be between 0-100%")
        if not (0 <= self.final_protein_content <= 100):
            raise ValidationError("Final protein content must be between 0-100%")
        if not (0 <= self.initial_moisture_content <= 100):
            raise ValidationError("Initial moisture content must be between 0-100%")
        if not (0 <= self.final_moisture_content <= 100):
            raise ValidationError("Final moisture content must be between 0-100%")
        if self.final_moisture_content > self.initial_moisture_content:
            raise ValidationError("Final moisture content cannot be higher than initial moisture content")
        
        # Particle size validations
        if not (self.d10_particle_size <= self.d50_particle_size <= self.d90_particle_size):
            raise ValidationError("Particle sizes must be in order: D10 ≤ D50 ≤ D90")
        if any(size <= 0 for size in [self.d10_particle_size, self.d50_particle_size, self.d90_particle_size]):
            raise ValidationError("Particle sizes must be positive")
            
        # Economic parameter validations
        if self.discount_rate <= 0 or self.discount_rate >= 1:
            raise ValidationError("Discount rate must be between 0 and 1")
        if any(cost <= 0 for cost in [self.equipment_cost, self.maintenance_cost, 
                                    self.raw_material_cost, self.utility_cost, self.labor_cost]):
            raise ValidationError("All costs must be positive")
        if self.project_duration <= 0:
            raise ValidationError("Project duration must be positive")
        if self.production_volume <= 0:
            raise ValidationError("Production volume must be positive")
            
        # Environmental parameter validations
        if any(consumption < 0 for consumption in [self.electricity_consumption, 
                                                 self.cooling_consumption, 
                                                 self.water_consumption]):
            raise ValidationError("Consumption values cannot be negative")
            
        # Calculate moisture reduction
        self.moisture_reduction = self.initial_moisture_content - self.final_moisture_content

class AnalysisResult(models.Model):
    process = models.OneToOneField(ProcessAnalysis, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Technical Results
    protein_recovery = models.FloatField(
        null=True,
        help_text="Protein recovery rate in %"
    )
    separation_efficiency = models.FloatField(
        null=True,
        help_text="Overall separation efficiency in %"
    )
    particle_size_distribution = models.JSONField(
        null=True,
        help_text="Particle size distribution metrics (D10, D50, D90)"
    )
    process_efficiency = models.FloatField(
        null=True,
        help_text="Process efficiency metric in %"
    )
    
    # Economic Results
    capex = models.JSONField(
        null=True,
        help_text="Capital expenditure breakdown"
    )
    opex = models.JSONField(
        null=True,
        help_text="Operational expenditure breakdown"
    )
    npv = models.FloatField(
        null=True,
        help_text="Net Present Value in USD"
    )
    roi = models.FloatField(
        null=True,
        help_text="Return on Investment in %"
    )
    payback_period = models.FloatField(
        null=True,
        help_text="Payback period in years"
    )
    profitability_index = models.FloatField(
        null=True,
        help_text="Profitability index"
    )
    sensitivity_analysis = models.JSONField(
        null=True,
        help_text="Sensitivity analysis results"
    )
    
    # Environmental Results
    gwp = models.FloatField(
        null=True,
        help_text="Global Warming Potential in CO2eq"
    )
    hct = models.FloatField(
        null=True,
        help_text="Human Carcinogenic Toxicity in CTUh"
    )
    frs = models.FloatField(
        null=True,
        help_text="Fossil Resource Scarcity in kg oil eq"
    )
    water_consumption = models.FloatField(
        null=True,
        help_text="Water consumption impact in m3"
    )
    allocated_impacts = models.JSONField(
        null=True,
        help_text="Allocated environmental impacts"
    )
    
    # Eco-efficiency Results
    eco_efficiency_index = models.FloatField(
        null=True,
        help_text="Overall eco-efficiency index"
    )
    relative_performance = models.FloatField(
        null=True,
        help_text="Relative performance compared to baseline"
    )
    efficiency_metrics = models.JSONField(
        null=True,
        help_text="Detailed efficiency metrics"
    )
    
    class Meta:
        ordering = ['-timestamp']
        
    def clean(self):
        """Validate analysis results"""
        super().clean()
        
        # Validate percentage fields are between 0-100
        percentage_fields = [
            'protein_recovery',
            'separation_efficiency',
            'process_efficiency',
            'roi'
        ]
        for field in percentage_fields:
            value = getattr(self, field)
            if value is not None and not (0 <= value <= 100):
                raise ValidationError(f"{field} must be between 0-100%")
        
        # Validate non-negative fields
        non_negative_fields = [
            'npv',
            'payback_period',
            'profitability_index',
            'gwp',
            'hct',
            'frs',
            'water_consumption',
            'eco_efficiency_index'
        ]
        for field in non_negative_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field} cannot be negative")
        
        # Validate JSON fields have required keys
        if self.particle_size_distribution:
            required_keys = ['d10', 'd50', 'd90']
            if not all(key in self.particle_size_distribution for key in required_keys):
                raise ValidationError("Particle size distribution must include d10, d50, and d90")
        
        if self.capex:
            required_keys = ['equipment_cost', 'installation_cost', 'indirect_cost', 'total_capex']
            if not all(key in self.capex for key in required_keys):
                raise ValidationError("CAPEX must include all cost components")
        
        if self.opex:
            required_keys = ['utilities_cost', 'materials_cost', 'labor_cost', 'maintenance_cost', 'total_opex']
            if not all(key in self.opex for key in required_keys):
                raise ValidationError("OPEX must include all cost components")
                
        if self.allocated_impacts:
            required_keys = ['method', 'factors', 'results']
            if not all(key in self.allocated_impacts for key in required_keys):
                raise ValidationError("Allocated impacts must include method, factors, and results") 