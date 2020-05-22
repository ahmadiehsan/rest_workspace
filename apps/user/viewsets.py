from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.user import serializers
from helpers import viewsets as custom_viewsets


class UserViewSet(
    NestedViewSetMixin,
    custom_viewsets.WriteOnlyModelViewSet,
    custom_viewsets.ReadOnlyModelViewSet,
):
    serializer_class = serializers.UserMinimalSerializer
    serializer_detail_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id).all()
