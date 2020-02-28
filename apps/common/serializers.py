from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from apps.common.models import Comment
from apps.user.serializers import UserMinimalSerializer
from helpers.serializers import RecursiveField


class CommentMinimalSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    child = RecursiveField(source='child_set', many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'child')


class CommentSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    user_id = serializers.HiddenField(source='user', default=serializers.CurrentUserDefault())
    child = RecursiveField(source='child_set', many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'user_id',
            'text',
            'model_type',
            'model_id',
            'child',
            'parent'
        )
