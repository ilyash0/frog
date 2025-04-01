from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=120, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)
    avatar = models.ImageField(upload_to='images/avatars')

    def __str__(self):
        return self.name
