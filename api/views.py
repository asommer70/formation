from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
import json

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

    def patch(self, request, pk):
        if request.POST:
            post_data = request.POST
        else:
            post_data = json.loads(request.body)

        input = Input.objects.get(pk=pk)
        input.status = post_data['status']
        input.route = Route.objects.get(pk=post_data['route_id'])
        input.route_holder = User.objects.get(pk=post_data['route_holder'])
        input.route_sender = User.objects.get(pk=post_data['route_holder'])
        input.current_dest = Destination.objects.get(
            pk=post_data['current_dest_id'])
        input.step = post_data['step']
        input.save()

        return JsonResponse({'message': 'Input successfully updated.'})


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

    def post(self, request):
        post_data = json.loads(request.body)
        route = Route.objects.create(
            form_id=post_data['form_id'],
            user_id=post_data['user_id']
        )

        # Add the route to each Destination.
        for dest_id in post_data['dests']:
            dest = Destination.objects.get(pk=dest_id)
            dest.route = route
            dest.save()

        return JsonResponse({'message': 'Route successfully created.'})


class ListCreateDestination(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    authentication_classes = (TokenAuthentication,)


class RetrieveUpdateDestroyDestination(generics.UpdateAPIView,
                                       generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    authentication_classes = (TokenAuthentication,)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
