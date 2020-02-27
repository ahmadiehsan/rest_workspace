from django.contrib import admin

from blog.models import Category, BlogPost, Comment


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


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'id',
        'create_time',
        'modify_time',
        'title',
        'content',
        'image',
        'author',
    )
    list_filter = ('create_time', 'modify_time', 'author')
    raw_id_fields = ('categories',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'create_time',
        'modify_time',
        'user',
        'text',
        'blog_post',
        'parent',
    )
    list_filter = (
        'create_time',
        'modify_time',
        'user',
        'blog_post',
        'parent',
    )
