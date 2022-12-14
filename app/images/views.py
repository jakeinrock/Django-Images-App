"""
Views for images app.
"""
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
from .models import Image, BinaryImageLink, AccountType

from PIL import Image as Img

from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings

import os
from io import BytesIO


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
        if self.action == 'list':
            return ImageSerializer
        if self.action == 'get_link':
            return BinaryImageLinkSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new image."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='get-link')
    def get_link(self, request, pk=None):
        """Get expiring link for binary image."""
        user_account = AccountType.objects.filter(users=self.request.user)
        if user_account[0].link_to_binary:
            try:
                image = self.get_object()
                img_img = image.image
                expiring_link_time = int(request.data['expiring_time'])
                host = os.environ.get('ALLOWED_HOSTS')

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

                serializer = self.get_serializer(data=request.data)

                if serializer.is_valid():

                    binary_image = BinaryImageLink()
                    binary_image.binary_image = File(
                        ContentFile(temp_binary.read()),
                        binary_filename)
                    binary_image.user = self.request.user
                    binary_image.expiring_time = expiring_link_time
                    binary_image.save()

                    user_binaries = BinaryImageLink.objects.filter(
                        user=self.request.user).order_by('-id')
                    bin_info = {}
                    binary_path = str(user_binaries[0].binary_image)
                    bin_info['binary_image'] = str(
                        'http://'+host+':8000'+settings.MEDIA_URL+binary_path)
                    msg = bin_info
                    status_code = status.HTTP_200_OK

                else:
                    msg = serializer.errors
                    status_code = status.HTTP_400_BAD_REQUEST

            except Exception as err:
                msg = f'Some problems occured: {err}'
                status_code = status.HTTP_400_BAD_REQUEST

            finally:
                return Response(msg, status=status_code)

        else:
            msg = 'Method not allowed for user account type.'
            status_code = status.HTTP_400_BAD_REQUEST

            return Response(msg, status=status_code)
