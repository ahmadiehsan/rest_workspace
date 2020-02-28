import json

from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from apps.blog.models import Category, Article, Comment
from apps.blog.search_indexes import ArticleIndex
from apps.user.serializers import UserMinimalSerializer

COMMON_IGNORED_FIELDS = ('text',)


class CategoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'order')


class CategorySerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'order', 'parent')


class ArticleMinimalSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'modify_time', 'image', 'categories', 'author')


class ArticleSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    author = UserMinimalSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'modify_time', 'image', 'categories', 'content', 'author')


class ArticleSearchSerializer(HaystackSerializer):
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    @staticmethod
    def get_author(obj):
        return json.loads(obj.author)

    @staticmethod
    def get_categories(obj):
        return json.loads(obj.categories)

    class Meta:
        ignore_fields = COMMON_IGNORED_FIELDS + ('autocomplete',)
        index_classes = (ArticleIndex,)
        fields = ('title', 'content', 'image', 'author', 'categories', 'autocomplete')
        field_aliases = {'q': 'autocomplete'}


class CommentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text')


class CommentSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'article', 'parent')
