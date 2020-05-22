from django.contrib import admin

from apps.blog.models import Category, Article
from helpers.admin import BaseAdminModel


@admin.register(Category)
class CategoryAdmin(BaseAdminModel):
    list_display = ('title', 'parent')


@admin.register(Article)
class ArticleAdmin(BaseAdminModel):
    save_as = True
    search_fields = ('title',)
    list_display = ('title', 'author')
    list_filter = ('vip_only',)
    raw_id_fields = ('categories',)
