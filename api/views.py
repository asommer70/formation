from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .serializers import (
    FormSerializer,
    InputSerializer,
    UserSerializer,
    GroupSerializer,
    RouteSerializer,
    DestinationSerializer
)
from forms.models import Form
from inputs.models import Input
from routes.models import Route, Destination


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


class ListCreateRoute(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    authentication_classes = (TokenAuthentication,)


class ListCreateDestination(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    authentication_classes = (TokenAuthentication,)


class RetrieveUpdateDestroyDestination(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    authentication_classes = (TokenAuthentication,)
