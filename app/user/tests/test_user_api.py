"""
Tests for user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user:token')
IMAGES_URL = reverse('image-list')

def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='testpass123')

        payload = {'email': 'test@example.com', 'password': 'invalidpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_image_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(IMAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
