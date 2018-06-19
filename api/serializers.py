from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from inputs.models import Input
from forms.models import Form


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'email')
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name',)
        model = Group


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
