"""
Serializers for images app.
"""
from rest_framework import serializers

from images.models import Image, AccountType, BinaryImageLink


class BinaryImageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryImageLink
        fields = ['id', 'expiring_time', ]
        read_only_fields = ['id', ]
        extra_kwargs = {'expiring_time': {'required': 'True'}}

    def validate(self, data):
        """
        Check if provided link expiration time is in range between 300 and 30000.
        """
        if int(data['expiring_time']) <= 299 or int(data['expiring_time']) >= 30001 or int(data['expiring_time']) % 300 != 0:
            raise serializers.ValidationError({
                "Expiration time should be a multiplication of 300sec(5min) and should be in range between 300 and 30000 seconds"})
        return data


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'thumbnail_size1', 'thumbnail_size2']
        read_only_fields = ['id', 'thumbnail_size1', 'thumbnail_size2']
        extra_kwargs = {'image': {'required': 'True'}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        check = AccountType.objects.filter(users=self.context['request'].user)
        if check[0].link_to_original is False:
            data.pop('image', None)
        if check[0].thumb_size2 is None:
            data.pop('thumbnail_size2', None)
        return data
