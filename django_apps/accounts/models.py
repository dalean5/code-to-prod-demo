from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password, **kwargs):
        if not email:
            raise ValueError("You must provide an email address")
        if not name:
            raise ValueError("You must provide a name")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned is_staff=True")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned is_superuser=True")
        if kwargs.get("is_active") is not True:
            raise ValueError("Superuser must be assigned is_active=True")

        return self.create_user(email, name, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
    ]

    objects = CustomUserManager()
