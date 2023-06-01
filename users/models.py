from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


BUSINESS_TYPE_CHOICES = [
    ("registed", "Registered"),
    ("starter", "Starter"),
]


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(
        max_length=100, choices=BUSINESS_TYPE_CHOICES, default="starter"
    )

    def __str__(self):
        return self.email
