from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .serializers import (
    FormSerializer,
    InputSerializer,
    UserSerializer,
    GroupSerializer
)
from forms.models import Form
from inputs.models import Input


class ListCreateForm(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    authentication_classes = (TokenAuthentication,)


class RetrieveUpdateDestroyForm(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    authentication_classes = (TokenAuthentication,)


class ListCreateInput(generics.ListCreateAPIView):
    queryset = Input.objects.all()
    serializer_class = InputSerializer
    authentication_classes = (TokenAuthentication,)


class RetrieveUpdateDestroyInput(generics.RetrieveUpdateDestroyAPIView):
    queryset = Input.objects.all()
    serializer_class = InputSerializer
    authentication_classes = (TokenAuthentication,)


class ListCreateUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)


class ListCreateGroup(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (TokenAuthentication,)
