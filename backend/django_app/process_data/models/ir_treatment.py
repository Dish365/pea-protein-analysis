from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class IRTreatmentProcess(models.Model):
    """
    IR treatment process configuration and parameters.
    
    Process Parameters:
    -----------------
    1. IR Heater:
       - Power density
       - Wavelength
       - Treatment time
    
    2. Material Properties:
       - Surface temperature
       - Moisture content
    """
    
    # Process identification
    process_id = models.CharField(max_length=50, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # IR parameters
    power_density = models.FloatField(
        validators=[MinValueValidator(2), MaxValueValidator(10)],
        help_text="Power density in kW/m²"
    )
    wavelength = models.FloatField(
        validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="IR wavelength in μm"
    )
    treatment_time = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(15)],
        help_text="Treatment time in minutes"
    )
    
    # Material properties
    surface_temperature = models.FloatField(
        validators=[MinValueValidator(30), MaxValueValidator(150)],
        help_text="Surface temperature in °C"
    )
    moisture_content = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text="Material moisture content in %"
    )
    
    class Meta:
        app_label = 'process_data'
        db_table = 'ir_treatment_process'
        ordering = ['-timestamp']
