from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_female = models.BooleanField(default=True)  # True: 여성, False: 남성
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    nickname = models.CharField(max_length=30, unique=True)
    birth_date = models.DateField()
    address = models.CharField(max_length=255)
    interests = models.ManyToManyField('Interest', blank=True)
    terms_agreement = models.BooleanField(default=False)

    # related_name 속성 추가
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
        related_query_name="custom_user",
    )

class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
