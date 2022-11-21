"""
Tests for images APIs.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.base import File

from rest_framework import status
from rest_framework.test import APIClient

from PIL import Image as Img
from PIL import ImageFile

from images.serializers import ImageSerializer
from images.models import (
    AccountType,
    User,
    Image,
)

from io import BytesIO
import tempfile
import os
from urllib import request as ulreq

IMAGES_URL = reverse('image-list')

def detail_url(image_id):
    """Create and return an image detail URL."""
    return reverse('image-detail', args=[image_id])

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_account_type(type):
    """Create and return new account type."""
    if type == 'Basic':
        params = {
            'title': 'Basic',
            'is_basic': True,
            'thumb_size1': 200,
    }
    if type == 'Premium':
        params = {
            'title': 'Premium',
            'is_premium': True,
            'thumb_size1': 400,
            'thumb_size2': 200,
            'link_to_original': True,
    }
    if type == 'Enterprise':
        params = {
            'title': 'Enterprise',
            'is_enterprise': True,
            'thumb_size1': 400,
            'thumb_size2': 200,
            'link_to_original': True,
            'link_to_binary': True,
    }
    if type == 'Custom':
        params = {
            'title': 'Custom',
            'is_custom': True,
            'thumb_size1': 300,
            'thumb_size2': 600,
            'link_to_original': True,
            'link_to_binary': True,
    }

    account_type = AccountType.objects.create(**params)

    return account_type

def get_image_file(name='test.png', ext='png', size=(800, 800), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Img.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)

    return File(file_obj, name=name)


class ImageUploadTests(TestCase):
    """Test for the image upload API."""

    def setUp(self):
        self.client = APIClient()

        basic = create_account_type(type='Basic')

        self.user = create_user(
            email='username@example.com',
            password='pass123',
            account_type=basic)

        self.client.force_authenticate(self.user)

    def test_upload_image(self):
        """Test uploading an image."""
        image = get_image_file()
        payload = {'title': 'sample image', 'image': image}
        res = self.client.post(IMAGES_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('thumbnail_size1', res.data)
        user_images = Image.objects.filter(user=self.user)
        self.assertEqual(user_images.count(), 1)

    def test_get_images(self):
        """Test retrieving a list of images."""
        Image.objects.create(
            user=self.user,
            title='sample1',
            image=get_image_file(),
        )
        Image.objects.create(
            user=self.user,
            title='sample2',
            image=get_image_file(),
        )

        res = self.client.get(IMAGES_URL)

        images = Image.objects.all().order_by('-id')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(images.count(), 2)


    def test_get_detail_image(self):
        """Test retrieving a detail image."""
        image = Image.objects.create(
            user=self.user,
            title='sample',
            image=get_image_file(),
        )

        url = detail_url(image.id)
        res = self.client.get(url)

        self.assertIn('title', res.data)
        self.assertIn('thumbnail_size1', res.data)
        self.assertNotIn('image', res.data)

    def test_delete_image(self):
        """Test deleting an image."""
        image = Image.objects.create(
            user=self.user,
            title='sample',
            image=get_image_file(),
        )

        url = detail_url(image.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Image.objects.filter(id=image.id).exists())

    def test_upload_invalid_type_image_bad_request(self):
        """Test uploading invalid type of image."""
        with tempfile.NamedTemporaryFile(suffix='.gif') as image_file:
            img = Img.new('RGB', (10, 10))
            img.save(image_file, format='GIF')
            image_file.seek(0)

            payload = {'title': 'sample image', 'image': image_file}
            res = self.client.post(IMAGES_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        payload = {'title': 'sample image', 'image': 'notanimage'}
        res = self.client.post(IMAGES_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_allowed_properties_not_in_response_data(self):
        """Test if Enterprise Account Type properties are not visible for
        Basic Account Type user."""
        image = get_image_file()

        payload = {'title': 'sample image', 'image': image}
        res = self.client.post(IMAGES_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('image', res.data)
        self.assertNotIn('thumbnail_size2', res.data)

    def test_user_cant_list_other_user_images(self):
        """Test if user can't list other user image."""
        other_user = create_user(
            email='username2@example.com',
            password='pass1234',
            account_type=create_account_type(type='Enterprise'))

        Image.objects.create(
            user=self.user,
            title='sample',
            image=get_image_file())

        other_user_images = Image.objects.filter(user=other_user)
        self.assertEqual(other_user_images.count(), 0)

    def test_delete_other_users_image_error(self):
        """Test trying to delete another users image gives error."""
        other_user = create_user(
            email='username2@example.com',
            password='pass1234',
            account_type=create_account_type(type='Enterprise'))

        image = Image.objects.create(
            user=other_user,
            title='sample',
            image=get_image_file())

        url = detail_url(image.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Image.objects.filter(id=image.id).exists())

    def test_user_cant_get_detail_image_from_other_user(self):
        """Test user can't get details about other user image."""
        other_user = create_user(
            email='username2@example.com',
            password='pass1234',
            account_type=create_account_type(type='Enterprise'))

        other_user_image = Image.objects.create(
            user=other_user,
            title='sample',
            image=get_image_file(),
        )

        url = detail_url(other_user_image.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn(other_user_image.title, res.data)

    def test_thumb_size_is_correct(self):
        """Test if size of created thumbnail is equal to user account type
        thumb_size property."""
        image = get_image_file()
        payload = {'title': 'sample image', 'image': image}
        res = self.client.post(IMAGES_URL, payload, format='multipart')

        thumb = Image.objects.filter(user=self.user)[0].thumbnail_size1

        im = Img.open(thumb)
        width, height = im.size

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('thumbnail_size1', res.data)
        self.assertEqual(height, AccountType.objects.filter(users=self.user)[0].thumb_size1)
