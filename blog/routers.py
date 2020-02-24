from rest_workspace.routers import router

from blog import viewsets

router.register(r'users',
                viewsets.UserViewSet,
                basename='user')

router.register(r'categories',
                viewsets.CategoryViewSet,
                basename='category').register(r'posts',
                                              viewsets.BlogPostViewSet,
                                              basename='category-posts',
                                              parents_query_lookups=['categories'])

router.register(r'posts',
                viewsets.BlogPostViewSet,
                basename='post').register(r'comments',
                                          viewsets.CommentViewSet,
                                          basename='post-comments',
                                          parents_query_lookups=['blog_post'])

router.register(r'comments', viewsets.CommentViewSet, basename='comment')
