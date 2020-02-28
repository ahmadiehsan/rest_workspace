from rest_framework import mixins, viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from apps.common import serializers
from apps.common.models import Comment


class CommentViewSet(
    NestedViewSetMixin,
    DetailSerializerMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = serializers.CommentMinimalSerializer
    serializer_detail_class = serializers.CommentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_detail_class
        return super().get_serializer_class()
