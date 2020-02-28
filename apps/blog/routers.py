from apps.blog import viewsets
from rest_workspace.routers import ROUTER, SEARCH_ROUTER

ROUTER.register(
    r'categories',
    viewsets.CategoryViewSet,
    basename='category'
).register(
    r'articles',
    viewsets.ArticleViewSet,
    basename='category-articles',
    parents_query_lookups=['categories']
)

ROUTER.register(r'articles', viewsets.ArticleViewSet, basename='article')

SEARCH_ROUTER.register(r'articles', viewsets.ArticleSearchViewSet, basename='article-search')
