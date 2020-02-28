from django.contrib.auth.models import User
from django.db import models

from apps.common.models import Comment
from helpers.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    order = models.IntegerField(default=999)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title


class Article(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to='articles_image', null=True, blank=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def comments(self):
        return Comment.objects.filter(model_type='article', model_id=self.id)

    def __str__(self):
        return self.title
