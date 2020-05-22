import json

from drf_haystack.serializers import HaystackSerializer, HaystackFacetSerializer
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from apps.blog.models import Category, Article
from apps.blog.search_indexes import ArticleIndex
from apps.common.serializers import CommentMinimalSerializer
from apps.user.serializers import UserMinimalSerializer
from helpers.serializers import CustomFacetFieldSerializer


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
        fields = ('id', 'title', 'modify_time_formatted', 'image', 'author', 'categories', 'vip_only')


class ArticleSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    author = UserMinimalSerializer()
    comments = CommentMinimalSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'modify_time_formatted', 'image', 'author', 'categories', 'comments', 'content', 'vip_only')


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
            'modify_time_formatted',
            'image',
            'author',
            'categories',
            'author_index',
            'categories_index',
            'autocomplete',
            'vip_only'
        )

        # for converting /?autocomplete= to /?q=
        field_aliases = {
            'q': 'autocomplete',
            'author': 'author_index',
            'categories': 'categories_index'
        }


class ArticleFacetSerializer(HaystackFacetSerializer):
    serialize_objects = True
    facet_field_serializer_class = CustomFacetFieldSerializer

    class Meta:
        index_classes = (ArticleIndex,)
        fields = (
            'title',
            'modify_time_formatted',
            'image',
            'author',
            'categories'
        )
        field_options = {
            'author_index': {},
            'categories_index': {},
        }
