from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from .managers import CustomUserManager

# from datetime import timedelta


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    kudos_count = models.PositiveIntegerField(default=3)
    kudos_last_reset = models.DateTimeField(default=now)

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # Change related_name to avoid conflicts
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # Change related_name
        blank=True,
    )

    def __str__(self):
        return f"{self.email} ({self.organization.name if self.organization else 'No Organization'})"


class Kudos(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kudos_given",
    )
    sender_first_name = models.CharField(max_length=255, null=True, blank=True)
    sender_last_name = models.CharField(max_length=255, null=True, blank=True)

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kudos_received",
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Ensure kudos are given within the same organization."""
        if self.sender.organization != self.receiver.organization:
            raise ValidationError(
                "Users must belong to the same organization to give kudos."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.message}"
