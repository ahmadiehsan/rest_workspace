from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin

from apps.user.models import UserAdditionalData


class UserAdditionalDataSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(min_length=10)

    class Meta:
        model = UserAdditionalData
        fields = ('id', 'phone_number', 'avatar')


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class UserSerializer(PartialUpdateSerializerMixin, serializers.ModelSerializer):
    user_additional_data = UserAdditionalDataSerializer(source='user_ad')
    first_name = serializers.CharField(max_length=5, allow_blank=True)
    last_name = serializers.CharField(default='test', allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'user_additional_data')

    @transaction.atomic
    def create(self, validated_data):
        user_ad_validated_data = validated_data.pop('user_ad')
        user = User.objects.create(**validated_data)
        UserAdditionalData.objects.create(**user_ad_validated_data, user=user)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        user_ad_validated_data = validated_data.pop('user_ad', {})
        user_ad = instance.user_ad

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        for key, value in user_ad_validated_data.items():
            setattr(user_ad, key, value)
        user_ad.save()

        return instance
