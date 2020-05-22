from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from helpers.models import BaseModel


class UserAdditionalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_ad', verbose_name=_('user'))
    avatar = models.ImageField(upload_to='users_avatar', null=True, blank=True, verbose_name=_('avatar'))
    phone_number = models.CharField(max_length=30, unique=True, verbose_name=_('phone_number'))


class VipAccount(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vip_data', verbose_name=_('user'))
    is_active = models.BooleanField(verbose_name=_('is_active'))

    def __str__(self):
        if self.is_active:
            return "{} is VIP user".format(self.user)
        return "{}'s VIP account is deactivated".format(self.user)
