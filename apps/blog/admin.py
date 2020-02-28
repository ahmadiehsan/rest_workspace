from django.contrib import admin

from apps.blog.models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'create_time',
        'modify_time',
        'title',
        'parent',
        'order',
    )
    list_filter = ('create_time', 'modify_time', 'parent')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'id',
        'title',
        'modify_time',
    )
    list_filter = ('create_time', 'modify_time')
    raw_id_fields = ('categories',)
