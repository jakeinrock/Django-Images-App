"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
