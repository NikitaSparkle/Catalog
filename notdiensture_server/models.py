from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Country(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=60)


class EmergencyServes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False)
    phone_number = models.CharField(max_length=16)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(null=False, unique=True)
    phone_number = models.CharField(max_length=16, unique=True, null=False)
    county = models.ForeignKey(Country, on_delete=models.CASCADE)


