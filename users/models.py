from django.contrib.auth.models import AbstractUser
from django.db import models

# в базовой модели AbstractUser поля first_name, last_name имеют ограничение в 150 символов
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
