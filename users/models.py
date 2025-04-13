from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True,blank=True)
    city = models.CharField(max_length=30,null=True,blank=True)
    region = models.CharField(max_length=30,null=True,blank=True)
    countryside = models.CharField(max_length=30,null=True,blank=True)
    avatar = models.ImageField(upload_to='profile_images/',default='images/ava-img.jpeg')

    def __str__(self):
        return self.username