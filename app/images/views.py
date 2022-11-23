"""
Views for images app.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ImageSerializer, BinaryImageLinkSerializer
from .models import Image, AccountType, BinaryImageLink

from PIL import Image as Img

from django.core.files import File

import os
from io import BytesIO

from django.core.files.base import ContentFile


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

    @action(methods=['POST'], detail=True, url_path='get-link')
    def get_link(self, request, pk=None):
        """Get expiring link for binary image."""
        try:
            # serializer = BinaryImageLinkSerializer
            image = self.get_object()
            img_img = image.image
            expiring_link_time = request.data['expiring_time']

            img = Img.open(img_img).convert('1')

            binary_name, binary_extension = os.path.splitext(img_img.name)
            binary_extension = binary_extension.lower()

            binary_filename = binary_name + '_binary' + binary_extension

            if binary_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif binary_extension == '.png':
                FTYPE = 'PNG'

            """Save binary image."""
            temp_binary = BytesIO()
            img.save(temp_binary, FTYPE)
            temp_binary.seek(0)

            binary_image = BinaryImageLink()
            binary_image.binary_image = File(ContentFile(temp_binary.read()), binary_filename)
            binary_image.user = self.request.user
            binary_image.expiring_time = expiring_link_time
            binary_image.save()

            user_binaries = BinaryImageLink.objects.filter(user=self.request.user).order_by('-id')
            bin_info = {}
            binary_path = str(user_binaries[0].binary_image)
            bin_info['binary_image'] = binary_path
            bin_info['created_at'] = user_binaries[0].created_at
            bin_info['expiration_date'] = user_binaries[0].expiration_date
            msg = bin_info
            status_code = status.HTTP_200_OK

        except Exception as err:
            msg = f'Some problems occured: {err}'
            status_code = status.HTTP_400_BAD_REQUEST

        finally:
            return Response(msg, status=status_code)
    # @action(methods=['GET'], detail=True, url_path='get-link')
    # def get_link(self, request, pk=None):
    #     """Get expiring link for binary image."""
    #     try:
    #         image = self.get_object()
    #         img_img = image.image

    #         binary_image = BinaryImageLink()
    #         binary_image.binary_image = File(img_img, img_img.name)
    #         binary_image.user = self.request.user
    #         binary_image.save()

    #         user_binaries = BinaryImageLink.objects.filter(user=self.request.user).order_by('-id')
    #         bin_image = {}
    #         binary_path = str(user_binaries[0].binary_image)
    #         bin_image['binary_image'] = binary_path
    #         msg = bin_image
    #         status_code = status.HTTP_200_OK

    #     except Exception as err:
    #         msg = f'Some problems occured: {err}'
    #         status_code = status.HTTP_400_BAD_REQUEST

    #     finally:
    #         return Response(msg, status=status_code)
