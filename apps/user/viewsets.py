from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, permissions
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from apps.user import serializers


class UserViewSet(NestedViewSetMixin,
                  DetailSerializerMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.UserMinimalSerializer
    serializer_detail_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id).all()

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_detail_class
        return super().get_serializer_class()
