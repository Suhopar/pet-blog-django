from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    """

    Advanced user model(CustomUser) with roles.

    """
    ROLE_CHOICES = [
        ('user', 'User (Default)'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    usual_ban = models.BooleanField(default=False)
    absolute_ban = models.BooleanField(default=False)
    user_about = models.CharField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True,
        blank=True, default='profile_images/profile_image_default.jpg')

def __str__(self):
        return self.username
