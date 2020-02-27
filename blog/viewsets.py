from django.contrib.auth.models import User
from django_filters import rest_framework as django_filters
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import filters as drf_filters
from rest_framework import viewsets, mixins, permissions
from rest_framework_extensions.mixins import DetailSerializerMixin, NestedViewSetMixin

from blog import filters
from blog import permissions as custom_permissions
from blog import serializers
from blog.models import Category, BlogPost, Comment


class UserViewSet(NestedViewSetMixin,
                  DetailSerializerMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.UserMinimalSerializer
    serializer_detail_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id).all()

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_detail_class
        return super().get_serializer_class()


class CategoryViewSet(NestedViewSetMixin, DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryMinimalSerializer
    serializer_detail_class = serializers.CategorySerializer


class BlogPostViewSet(NestedViewSetMixin, DetailSerializerMixin, viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostMinimalSerializer
    serializer_detail_class = serializers.BlogPostSerializer
    permission_classes = (custom_permissions.IsBlogPostOwnerOrReadOnly,
                          permissions.DjangoModelPermissionsOrAnonReadOnly)
    filter_backends = (drf_filters.SearchFilter,
                       drf_filters.OrderingFilter,
                       django_filters.DjangoFilterBackend)

    # drf_filters (OrderingFilter)
    ordering_fields = ('title',)

    # drf_filters (SearchFilter)
    search_fields = ('title',)

    # django_filter
    filter_class = filters.BlogPostFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_detail_class
        return super().get_serializer_class()


class BlogPostSearchViewSet(HaystackViewSet):
    index_models = (BlogPost,)
    serializer_class = serializers.BlogPostSearchSerializer
    permission_classes = ()  # prevent from exception ('SearchQuerySet' object has no attribute 'model')


class CommentViewSet(NestedViewSetMixin,
                     DetailSerializerMixin,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentMinimalSerializer
    serializer_detail_class = serializers.CommentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_detail_class
        return super().get_serializer_class()
