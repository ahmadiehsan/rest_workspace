import json

from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from apps.blog.models import Category, Article
from apps.blog.search_indexes import ArticleIndex
from apps.common.serializers import CommentMinimalSerializer
from apps.user.serializers import UserMinimalSerializer
from helpers.utils import to_jalali_datetime


class CategoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class CategorySerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'order', 'parent')


class ArticleMinimalSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'modify_time', 'image', 'author', 'categories')


class ArticleSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    author = UserMinimalSerializer()
    comments = CommentMinimalSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'modify_time', 'image', 'author', 'categories', 'comments', 'content')


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
        ignore_fields = ('text', 'author_index', 'categories_index', 'autocomplete')
        index_classes = (ArticleIndex,)
        fields = ('title',
                  'modify_time',
                  'image',
                  'author',
                  'categories',
                  'author_index',
                  'categories_index',
                  'autocomplete')

        # for converting /?autocomplete= to /?q=
        field_aliases = {'q': 'autocomplete',
                         'author': 'author_index',
                         'categories': 'categories_index'}
