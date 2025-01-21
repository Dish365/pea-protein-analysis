from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DRFValidationError

def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, DjangoValidationError):
            response = Response({
                'error': 'Validation Error',
                'detail': exc.message_dict if hasattr(exc, 'message_dict') else exc.messages
            }, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, IntegrityError):
            response = Response({
                'error': 'Database Error',
                'detail': str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, Exception):
            response = Response({
                'error': 'Internal Server Error',
                'detail': str(exc)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Ensure all validation errors have a consistent format
    if isinstance(exc, DRFValidationError):
        if isinstance(response.data, dict):
            response.data = {
                'error': 'Validation Error',
                'detail': response.data
            }
        else:
            response.data = {
                'error': 'Validation Error',
                'detail': {'non_field_errors': response.data}
            }

    return response 