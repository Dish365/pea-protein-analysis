from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class RFTreatmentProcess(models.Model):
    """
    RF treatment process configuration and parameters.
    
    Process Parameters:
    -----------------
    1. RF Generator:
       - Power
       - Frequency
       - Treatment time
    
    2. Material Properties:
       - Moisture content
       - Dielectric properties
    """
    
    # Process identification
    process_id = models.CharField(max_length=50, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # RF parameters
    power = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)],
        help_text="RF power in kW"
    )
    frequency = models.FloatField(
        default=27.12,
        help_text="RF frequency in MHz"
    )
    treatment_time = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Treatment time in minutes"
    )
    
    # Material properties
    moisture_content = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text="Material moisture content in %"
    )
    dielectric_constant = models.FloatField(
        validators=[MinValueValidator(1)],
        help_text="Dielectric constant"
    )
    loss_factor = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Dielectric loss factor"
    )
    
    class Meta:
        db_table = 'rf_treatment_process'
        ordering = ['-timestamp']
