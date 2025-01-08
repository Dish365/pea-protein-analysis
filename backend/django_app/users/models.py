from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model for the application."""
    email = models.EmailField(unique=True)
    is_researcher = models.BooleanField(default=False)
    is_analyst = models.BooleanField(default=False)
    
    # Add any additional fields you need
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users' 