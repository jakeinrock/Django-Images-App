"""
Views for images app.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    mixins,
)

from .serializers import ImageSerializer
from .models import Image, AccountType

class ImageViewSet(mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """View for manage images APIs."""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve images for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'upload':
            return ImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new image."""
        serializer.save(user=self.request.user)
