from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('create_time',)


class UserAdditionalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_ad')
    avatar = models.ImageField(upload_to='users_avatar', null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)


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

    def __str__(self):
        return self.title


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.user, self.article)
