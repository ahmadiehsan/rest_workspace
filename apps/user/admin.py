from django.contrib import admin
from django.contrib.auth.models import User

from apps.user.models import UserAdditionalData

# unregistering django default user admin model
admin.site.unregister(User)


class UserAdditionalDataInline(admin.StackedInline):
    model = UserAdditionalData
    extra = 1
    min_num = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login', 'date_joined')
    inlines = (UserAdditionalDataInline,)
