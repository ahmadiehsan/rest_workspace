from apps.blog import viewsets
from rest_workspace.routers import ROUTER, SEARCH_ROUTER

ROUTER.register(r'categories',
                viewsets.CategoryViewSet,
                basename='category').register(r'articles',
                                              viewsets.ArticleViewSet,
                                              basename='category-articles',
                                              parents_query_lookups=['categories'])

ROUTER.register(r'articles',
                viewsets.ArticleViewSet,
                basename='article').register(r'comments',
                                             viewsets.CommentViewSet,
                                             basename='article-comments',
                                             parents_query_lookups=['article'])

SEARCH_ROUTER.register(r'articles', viewsets.ArticleSearchViewSet, basename='article-search')

ROUTER.register(r'comments', viewsets.CommentViewSet, basename='comment')
