"""
Database models.
"""
import uuid
import os

import os.path
from PIL import Image as Img
from io import BytesIO

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator

def create_uuid_filename(filename):
    """Generate uuid file name."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return filename

def image_file_path(instance, filename):
    """Generate file path for image."""
    return os.path.join('uploads', 'images', create_uuid_filename(filename))

def thumb_file_path(instance, filename):
    """Generate file path for thumbnail."""
    return os.path.join('uploads', 'thumbs', create_uuid_filename(filename))


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class AccountType(models.Model):
    """Account Type object."""
    title = models.CharField(max_length=50, unique=True)
    is_basic = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_enterprise = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    thumb_size1 = models.IntegerField(blank=False)
    thumb_size2 = models.IntegerField(blank=True, null=True)
    link_to_original = models.BooleanField(default=False)
    link_to_binary = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    account_type = models.ForeignKey(
        AccountType,
        related_name='users',
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        blank=False,
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Image(models.Model):
    """Image object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='images',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(
        null=True, blank=False,
        upload_to=image_file_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])
            ]
        )
    thumbnail_size1 = models.ImageField(null=True, blank=True, upload_to=thumb_file_path)
    thumbnail_size2 = models.ImageField(null=True, blank=True, upload_to=thumb_file_path)

    def save(self, *args, **kwargs):
        """Save instance."""

        if not self.make_thumbnail():
            """Set to a default thumbnail."""
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Image, self).save(*args, **kwargs)

    def make_thumbnail(self):
        """Generate a thumbnail from a photo."""
        thumb_sizes = {}
        t1 = AccountType.objects.filter(users=self.user)[0].thumb_size1
        t2 = AccountType.objects.filter(users=self.user)[0].thumb_size2
        if t1 is not None:
            thumb_sizes['thumb1'] = t1
        if t2 is not None:
            thumb_sizes['thumb2'] = t2

        for thumb_no in thumb_sizes.keys():
            size = thumb_sizes[thumb_no]
            img = Img.open(self.image)
            img.thumbnail((size, size), Img.ANTIALIAS)

            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_extension = thumb_extension.lower()

            thumb_filename = thumb_name + '_thumb' + thumb_extension

            if thumb_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False

            """Save thumbnail to in-memory file as StringIO"""
            temp_thumb = BytesIO()
            img.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)

            if thumb_no == 'thumb1':
                self.thumbnail_size1.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            if thumb_no == 'thumb2':
                self.thumbnail_size2.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

        return True

    def __str__(self):
        return self.title
