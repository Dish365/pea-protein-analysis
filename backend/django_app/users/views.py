from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that includes user role information."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            response.data['user'] = {
                'username': user.username,
                'is_researcher': user.is_researcher,
                'is_analyst': user.is_analyst,
            }
        return response

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user."""
    # Add your registration logic here
    pass 