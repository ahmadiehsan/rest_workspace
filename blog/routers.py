from rest_workspace.routers import ROUTER, SEARCH_ROUTER

from blog import viewsets

ROUTER.register(r'users',
                viewsets.UserViewSet,
                basename='user')

ROUTER.register(r'categories',
                viewsets.CategoryViewSet,
                basename='category').register(r'posts',
                                              viewsets.BlogPostViewSet,
                                              basename='category-posts',
                                              parents_query_lookups=['categories'])

ROUTER.register(r'posts',
                viewsets.BlogPostViewSet,
                basename='post').register(r'comments',
                                          viewsets.CommentViewSet,
                                          basename='post-comments',
                                          parents_query_lookups=['blog_post'])

SEARCH_ROUTER.register(r'posts', viewsets.BlogPostSearchViewSet, basename='post-search')

ROUTER.register(r'comments', viewsets.CommentViewSet, basename='comment')
