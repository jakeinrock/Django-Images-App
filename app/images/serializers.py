"""
Serializers for images app.
"""
from rest_framework import serializers

from images.models import Image, AccountType

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'thumbnail_size1', 'thumbnail_size2']
        read_only_fields = ['id', 'thumbnail_size1', 'thumbnail_size2']
        extra_kwargs = {'image': {'required': 'True'}}

    # def _get_fields(self):
    #     """Hide fields which user is not allowed to see."""
    #     fields = super().get_fields()
    #     check = AccountType.objects.filter(users=self.context['request'].user)
    #     if check[0].link_to_original is False:
    #         fields.pop('image', None)
    #     if check[0].thumb_size2 is None:
    #         fields.pop('thumbnail_size2', None)

    #     return fields
    def to_representation(self, instance):
        data = super().to_representation(instance)
        check = AccountType.objects.filter(users=self.context['request'].user)
        if check[0].link_to_original is False:
            data.pop('image', None)
        if check[0].thumb_size2 is None:
            data.pop('thumbnail_size2', None)
        return data