from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.common import serializers
from apps.common.models import Comment
from helpers import viewsets as custom_viewsets


class CommentViewSet(
    NestedViewSetMixin,
    custom_viewsets.CreateOnlyModelViewSet,
    custom_viewsets.ReadOnlyModelViewSet,
):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = serializers.CommentMinimalSerializer
    serializer_detail_class = serializers.CommentSerializer
