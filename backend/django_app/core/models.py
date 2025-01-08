from django.db import models
from django.conf import settings

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    efficiency = models.FloatField()
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2)
    energy_consumption = models.FloatField()  # kWh
    processing_capacity = models.FloatField()  # kg/h
    
    class Meta:
        verbose_name = 'equipment'
        verbose_name_plural = 'equipment'
        
    def __str__(self):
        return self.name

class ProcessStep(models.Model):
    PROCESS_TYPES = [
        ('baseline', 'Baseline'),
        ('rf', 'RF Treatment'),
        ('ir', 'IR Treatment'),
    ]
    
    name = models.CharField(max_length=100)
    process_type = models.CharField(max_length=20, choices=PROCESS_TYPES)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    order = models.PositiveIntegerField()
    input_mass = models.FloatField()  # kg
    output_mass = models.FloatField()  # kg
    protein_content = models.FloatField()  # %
    moisture_content = models.FloatField()  # %
    particle_size_d10 = models.FloatField()  # μm
    particle_size_d50 = models.FloatField()  # μm
    particle_size_d90 = models.FloatField()  # μm
    
    class Meta:
        ordering = ['process_type', 'order']
        
    def __str__(self):
        return f"{self.process_type} - {self.name}"

class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    process_type = models.CharField(max_length=20, choices=ProcessStep.PROCESS_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Technical Analysis Results
    protein_yield = models.FloatField()
    separation_efficiency = models.FloatField()
    
    # Economic Analysis Results
    capex = models.DecimalField(max_digits=12, decimal_places=2)
    opex = models.DecimalField(max_digits=12, decimal_places=2)
    npv = models.DecimalField(max_digits=12, decimal_places=2)
    roi = models.FloatField()
    
    # Environmental Analysis Results
    gwp = models.FloatField()  # Global Warming Potential
    hct = models.FloatField()  # Human Carcinogenic Toxicity
    frs = models.FloatField()  # Fossil Resource Scarcity
    wc = models.FloatField()   # Water Consumption
    
    class Meta:
        verbose_name = 'analysis'
        verbose_name_plural = 'analyses'
        
    def __str__(self):
        return f"{self.process_type} Analysis - {self.created_at}"
