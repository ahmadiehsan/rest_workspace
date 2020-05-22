from django.contrib import admin

from apps.common.models import Comment
from helpers.admin import BaseAdminModel


@admin.register(Comment)
class CommentAdmin(BaseAdminModel):
    list_display = ('user', 'text')
    list_filter = ('model_type', 'model_id')
