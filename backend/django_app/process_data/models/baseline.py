from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BaselineProcess(models.Model):
    """
    Baseline process configuration and parameters.
    
    Process Parameters:
    -----------------
    1. Air Classification:
       - Air flow rate
       - Classifier speed
       - Feed rate
    
    2. Process Conditions:
       - Temperature
       - Humidity
       - Pressure
    """
    
    # Process identification
    process_id = models.CharField(max_length=50, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Air classification parameters
    air_flow_rate = models.FloatField(
        validators=[MinValueValidator(10), MaxValueValidator(50)],
        help_text="Air flow rate in m³/h"
    )
    classifier_speed = models.FloatField(
        validators=[MinValueValidator(1000), MaxValueValidator(5000)],
        help_text="Classifier speed in rpm"
    )
    feed_rate = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Feed rate in kg/h"
    )
    
    # Process conditions
    temperature = models.FloatField(
        validators=[MinValueValidator(15), MaxValueValidator(35)],
        help_text="Process temperature in °C"
    )
    humidity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Relative humidity in %"
    )
    pressure = models.FloatField(
        validators=[MinValueValidator(0.8), MaxValueValidator(1.2)],
        help_text="Atmospheric pressure in bar"
    )
    
    class Meta:
        db_table = 'baseline_process'
        ordering = ['-timestamp']
