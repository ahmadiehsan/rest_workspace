from django_filters import rest_framework as django_filters
from drf_haystack import filters as drf_haystack_filters
from drf_haystack.mixins import MoreLikeThisMixin, FacetMixin
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import filters as drf_filters
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.blog import filters, permissions as custom_permissions, serializers
from apps.blog.models import Category, Article
from helpers import viewsets as custom_viewsets


class CategoryViewSet(NestedViewSetMixin, custom_viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryMinimalSerializer
    serializer_detail_class = serializers.CategorySerializer


class ArticleViewSet(NestedViewSetMixin, custom_viewsets.ModelViewSet):
    serializer_class = serializers.ArticleMinimalSerializer
    serializer_detail_class = serializers.ArticleSerializer
    permission_classes = (custom_permissions.ArticlePermissions,)
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

    def get_queryset(self):
        return Article.objects.by_user_perm(self.request.user)


class ArticleSearchViewSet(FacetMixin, MoreLikeThisMixin, HaystackViewSet):
    permission_classes = ()  # prevent from exception ('SearchQuerySet' object has no attribute 'model')

    # index option
    serializer_class = serializers.ArticleSearchSerializer
    filter_backends = (
        drf_haystack_filters.HaystackOrderingFilter,
        drf_haystack_filters.HaystackAutocompleteFilter,
    )
    ordering_fields = ('modify_time',)
    index_models = (Article,)

    # facet options
    facet_serializer_class = serializers.ArticleFacetSerializer
    facet_filter_backends = (drf_haystack_filters.HaystackFacetFilter,)
    facet_query_params_text = 'p'  # will effect on narrow_url
