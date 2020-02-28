from apps.user import viewsets
from rest_workspace.routers import ROUTER

ROUTER.register(r'users', viewsets.UserViewSet, basename='user')
