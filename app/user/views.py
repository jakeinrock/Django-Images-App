"""
Views for the user API.
"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    AuthTokenSerializer,
)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for use"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
