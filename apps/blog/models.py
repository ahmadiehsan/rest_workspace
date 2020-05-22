from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _

from apps.blog import rules as custom_rules
from apps.common.models import Comment
from helpers.models import BaseModel, BaseModelManager


class Category(BaseModel):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('parent'))
    order = models.IntegerField(default=999, verbose_name=_('order'))

    class Meta(BaseModel.Meta):
        ordering = ('order',)

    def __str__(self):
        return self.title


class ArticleManager(BaseModelManager):
    def by_user_perm(self, user):
        query = Q()

        # vip user check
        if not user.has_perm(Article.get_perm('view_vip')):
            query.add(Q(vip_only=False), Q.AND)

        own_result = self.not_deleted().filter(author_id=user.id)

        return self.not_deleted().filter(query) | own_result


class Article(BaseModel):
    title = models.CharField(max_length=150, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    image = models.ImageField(upload_to='articles_image', null=True, blank=True, verbose_name=_('image'))
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('author'))
    vip_only = models.BooleanField(default=False, verbose_name=_('vip_only'))

    objects = ArticleManager()

    @property
    def comments(self):
        return Comment.objects.filter(model_type='article', model_id=self.id)

    def __str__(self):
        return self.title

    class Meta(BaseModel.Meta):
        # django_rules permission checker logic
        rules_permissions = {
            'add': custom_rules.is_vip_or_editor,
            'change': custom_rules.is_author_or_editor,
            'delete': custom_rules.is_member_of_editors,
            'view_vip': custom_rules.is_vip_or_editor,
        }
