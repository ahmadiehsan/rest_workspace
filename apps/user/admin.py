from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.user.models import UserAdditionalData, VipAccount
from helpers.admin import BaseAdminModel


class UserAdditionalDataInline(admin.StackedInline):
    model = UserAdditionalData
    extra = 1
    min_num = 1


# unregistering django default user admin model
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (UserAdditionalDataInline,)


@admin.register(VipAccount)
class VipAccountAdmin(BaseAdminModel):
    search_fields = ('user',)
    list_display = ('user', 'is_active')
    list_filter = ('is_active',)
    raw_id_fields = ('user',)
