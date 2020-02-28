import json

from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from apps.blog.models import Category, Article
from apps.blog.search_indexes import ArticleIndex
from apps.common.serializers import CommentMinimalSerializer
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
        fields = ('id', 'title', 'modify_time', 'image', 'author')


class ArticleSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    author = UserMinimalSerializer()
    comments = CommentMinimalSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'modify_time', 'image', 'author', 'comments', 'categories', 'content')


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
