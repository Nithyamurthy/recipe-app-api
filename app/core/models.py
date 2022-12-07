"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields) # calls User model
        user.set_password(password)
        user.save(using=self._db) # best practice when you create new instance

        return user
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects=UserManager()

    USERNAME_FIELD='email'
    # Defines the field used for authentication by default djangouser model
    # We override that field to use email
