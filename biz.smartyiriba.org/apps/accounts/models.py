from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    class CustomerType(models.TextChoices):
        INDIVIDUAL = 'individual', 'Particulier'
        BUSINESS = 'business', 'Entreprise'
        NGO = 'ngo', 'Association / ONG'
        INSTITUTION = 'institution', 'Institution'
    customer_type = models.CharField(max_length=20, choices=CustomerType.choices, default=CustomerType.INDIVIDUAL)
    organization = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=2, choices=[('fr', 'Français'), ('en', 'English')], default='fr')
