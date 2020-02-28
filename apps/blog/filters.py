from django_filters import rest_framework as filters

from apps.blog.models import Article


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ('author',)
