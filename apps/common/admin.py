from django.contrib import admin

from apps.common.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'create_time',
        'modify_time',
        'user',
        'text',
        'model',
        'parent',
    )
    list_filter = (
        'create_time',
        'modify_time',
        'user',
        'model',
        'parent',
    )
