from apps.common import viewsets
from rest_workspace.routers import ROUTER

ROUTER.register(r'comments', viewsets.CommentViewSet, basename='comment')
