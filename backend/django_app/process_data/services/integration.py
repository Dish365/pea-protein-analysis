from typing import Dict, Any
from fastapi import HTTPException
import httpx
from django.conf import settings

class ServiceIntegrator:
    """
    Integrate Django process data services with FastAPI calculation services.
    
    Features:
    --------
    1. Service Discovery
    2. API Integration
    3. Error Handling
    4. Data Transformation
    """
    
    def __init__(self):
        self.fastapi_base_url = settings.FASTAPI_SERVICE_URL
        
    async def get_calculations(
        self,
        endpoint: str,
        data: Dict
    ) -> Dict:
        """Make async calls to FastAPI calculation service."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.fastapi_base_url}/{endpoint}",
                    json=data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Calculation service error: {str(e)}"
                )
    
    def transform_process_data(
        self,
        django_model: Any,
        include_related: bool = False
    ) -> Dict:
        """Transform Django model data for FastAPI service."""
        data = {}
        
        # Get model fields
        for field in django_model._meta.fields:
            value = getattr(django_model, field.name)
            data[field.name] = value
            
        # Include related data if requested
        if include_related:
            for related in django_model._meta.related_objects:
                related_name = related.get_accessor_name()
                related_data = getattr(django_model, related_name).all()
                data[related_name] = [
                    self.transform_process_data(item)
                    for item in related_data
                ]
                
        return data
    
    def validate_cross_service(
        self,
        data: Dict,
        validation_rules: Dict
    ) -> bool:
        """
        Ensure consistent validation across services.
        
        This prevents duplicate validation logic between Django and FastAPI.
        """
        from .validation import ProcessDataValidator
        
        validator = ProcessDataValidator()
        return validator.validate_process_data(data, validation_rules) 