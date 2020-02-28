from rest_framework import serializers

from helpers.utils import clean_phone_number


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class PhoneNumberField(serializers.Field):
    def to_representation(self, value):
        return str(value).replace('+98', '0')

    def to_internal_value(self, data):
        return clean_phone_number(data)
