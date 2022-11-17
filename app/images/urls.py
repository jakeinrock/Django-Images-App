"""
URL mappings for images app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from images.views import ImageViewSet

router = DefaultRouter()
router.register('image', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
