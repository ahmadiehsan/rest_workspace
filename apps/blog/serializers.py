import datetime
import json

from drf_haystack.serializers import HaystackSerializer, HaystackFacetSerializer
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from apps.blog.models import Category, Article
from apps.blog.search_indexes import ArticleIndex
from apps.common.serializers import CommentMinimalSerializer
from apps.user.serializers import UserMinimalSerializer


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
    more_like_this = serializers.HyperlinkedIdentityField(view_name="article-search-more-like-this", read_only=True)

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
        fields = (
            'title',
            'modify_time',
            'image',
            'author',
            'categories',
            'author_index',
            'categories_index',
            'autocomplete'
        )

        # for converting /?autocomplete= to /?q=
        field_aliases = {
            'q': 'autocomplete',
            'author': 'author_index',
            'categories': 'categories_index'
        }


class ArticleFacetSerializer(HaystackFacetSerializer):
    serialize_objects = True

    class Meta:
        index_classes = (ArticleIndex,)
        fields = (
            'title',
            'modify_time',
            'image',
            'author',
            'categories'
        )
        field_options = {
            "title": {},
            "author": {},
            "modify_time": {
                "start_date": datetime.datetime.now() - datetime.timedelta(days=3 * 365),
                "end_date": datetime.datetime.now(),
                "gap_by": "month",
                "gap_amount": 3
            }
        }
