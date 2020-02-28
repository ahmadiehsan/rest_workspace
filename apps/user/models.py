from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserAdditionalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_ad')
    avatar = models.ImageField(upload_to='users_avatar', null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
