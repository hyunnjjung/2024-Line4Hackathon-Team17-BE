from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female')
    nickname = models.CharField(max_length=30, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    interests = models.ManyToManyField('Interest', blank=True)

class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
