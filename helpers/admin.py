from django.contrib import admin
from django.utils.translation import ugettext as _

from helpers.models import BaseModel


class BaseAdminModel(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        for col in BaseModel.auto_cols:
            try:
                fields.remove(col)
            except Exception:
                pass
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (_('other data'), {
            'fields': (
                ('create_time_formatted', 'created_by'),
                ('modify_time_formatted', 'updated_by'),
                'is_deleted',
            )
        }),
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + (
            'created_by',
            'updated_by',
            'create_time_formatted',
            'modify_time_formatted'
        )

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return list_filter + ('is_deleted',)

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ('modify_date_formatted', 'is_deleted')
