from rest_framework import serializers
from inputs.models import Input
from forms.models import Form


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'content',
            'public'
        )
        model = Form


class InputSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        fields = (
            'id',
            'created_at',
            'updated_at',
            'form',
            'data',
            'status',
            'route_date',
            'user'
        )
        model = Input
