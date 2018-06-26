from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from inputs.models import Input
from forms.models import Form
from routes.models import Route, Destination


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


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'created_at',
            'updated_at',
            'form',
            'user',
            'group'
        )
        model = Route


class DestinationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField(required=False)
    group = GroupSerializer(required=False)
    group_id = serializers.IntegerField(required=False)

    class Meta:
        fields = (
            'id',
            'created_at',
            'updated_at',
            'route',
            'step',
            'user',
            'user_id',
            'group',
            'group_id'
        )
        model = Destination

    def update(self, instance, validated_data):
        try:
            user = User.objects.get(pk=validated_data['user_id'])
            if user:
                instance.user = user
                instance.save()
        except KeyError:
            pass

        try:
            group = Group.objects.get(pk=validated_data['group_id'])
            if group:
                instance.group = group
                instance.save()
        except KeyError:
            pass

        return instance
