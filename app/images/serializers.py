"""
Serializers for images app.
"""
from rest_framework import serializers

from images.models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'thumbnail_size1', 'thumbnail_size2']
        read_only_fields = ['id', 'thumbnail_size1', 'thumbnail_size2']
        extra_kwargs = {'image': {'required': 'True'}}
