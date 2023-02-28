from django.db import models

#https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#specifying-a-custom-user-model
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveBigIntegerField(null= True, blank= True)
