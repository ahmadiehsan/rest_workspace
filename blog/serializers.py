from django.contrib.auth.models import User
from django.db import transaction
from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from blog.models import Category, BlogPost, Comment, UserAdditionalData
from blog.search_indexes import BlogPostIndex


COMMON_IGNORED_FIELDS = ('text',)


class UserAdditionalDataSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(min_length=10)

    class Meta:
        model = UserAdditionalData
        fields = ('id', 'phone_number', 'avatar')


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class UserSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    user_additional_data = UserAdditionalDataSerializer(source='user_ad')
    first_name = serializers.CharField(max_length=5, allow_blank=True)
    last_name = serializers.CharField(default='test', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'user_additional_data')

    @transaction.atomic
    def create(self, validated_data):
        user_ad_validated_data = validated_data.pop('user_ad')
        user = User.objects.create(**validated_data)
        UserAdditionalData.objects.create(**user_ad_validated_data, user=user)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        user_ad_validated_data = validated_data.pop('user_ad', {})
        user_ad = instance.user_ad

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        for key, value in user_ad_validated_data.items():
            setattr(user_ad, key, value)
        user_ad.save()

        return instance


class CategoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'order')


class CategorySerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'order', 'parent')


class BlogPostMinimalSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer()

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'modify_time', 'image', 'categories', 'author')


class BlogPostSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    author = UserMinimalSerializer()

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'modify_time', 'image', 'categories', 'content', 'author')


class BlogPostSearchSerializer(HaystackSerializer):
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        instances = Category.objects.filter(id__in=obj.category_ids)
        return CategoryMinimalSerializer(instances, many=True).data

    class Meta:
        ignore_fields = COMMON_IGNORED_FIELDS
        index_classes = (BlogPostIndex,)
        fields = ('title', 'image', 'categories')


class CommentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text')


class CommentSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'blog_post', 'parent')
