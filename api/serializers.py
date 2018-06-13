from django.contrib.auth import get_user_model
from rest_framework import serializers
from inputs.models import Input
from forms.models import Form


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User


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
