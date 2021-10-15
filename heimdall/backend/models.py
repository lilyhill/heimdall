from django.core.exceptions import ValidationError
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)



admin.site.register(MyUser)