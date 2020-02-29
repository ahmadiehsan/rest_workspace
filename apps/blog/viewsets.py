from django_filters import rest_framework as django_filters
from drf_haystack import filters as drf_haystack_filters
from drf_haystack.mixins import MoreLikeThisMixin, FacetMixin
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import filters as drf_filters
from rest_framework import viewsets, permissions
from rest_framework_extensions.mixins import DetailSerializerMixin, NestedViewSetMixin

from apps.blog import filters, permissions as custom_permissions, serializers
from apps.blog.models import Category, Article


class CategoryViewSet(NestedViewSetMixin, DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryMinimalSerializer
    serializer_detail_class = serializers.CategorySerializer


class ArticleViewSet(NestedViewSetMixin, DetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleMinimalSerializer
    serializer_detail_class = serializers.ArticleSerializer
    permission_classes = (
        custom_permissions.IsArticleOwnerOrReadOnly,
        permissions.DjangoModelPermissionsOrAnonReadOnly
    )
    filter_backends = (
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    )

    # drf_filters (OrderingFilter)
    ordering_fields = ('title',)

    # drf_filters (SearchFilter)
    search_fields = ('title',)

    # django_filter
    filter_class = filters.ArticleFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_detail_class
        return super().get_serializer_class()


class ArticleSearchViewSet(FacetMixin, MoreLikeThisMixin, HaystackViewSet):
    permission_classes = ()  # prevent from exception ('SearchQuerySet' object has no attribute 'model')
    serializer_class = serializers.ArticleSearchSerializer
    filter_backends = (
        drf_haystack_filters.HaystackOrderingFilter,
        drf_haystack_filters.HaystackAutocompleteFilter,
    )
    ordering_fields = ('modify_time',)

    # index option
    index_models = (Article,)

    # facet options
    facet_serializer_class = serializers.ArticleFacetSerializer
    facet_filter_backends = (drf_haystack_filters.HaystackFacetFilter,)
    facet_query_params_text = 'p'  # will effect on narrow_url
