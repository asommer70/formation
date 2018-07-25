from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
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
from inputs.models import Input, Approval, Comment
from routes.models import Route, Destination
from inputs.emails import inbox_notification, route_notification


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
        if (post_data['route_holder'] != ''):
            input.route_holder = User.objects.get(pk=post_data['route_holder'])
        else:
            input.route_holder = None
        if (post_data['route_sender'] != ''):
            input.route_sender = User.objects.get(pk=post_data['route_sender'])
        else:
            input.route_sender = None
        input.save()

        
        # Send email to new route_holder.
        if input.status != 'archived':
            inbox_notification(input)
            
        # Inform the Input creator.
        if (self.request.user != input.user):
            route_notification(input)

        approval = Approval.objects.create(input=input, user=input.route_sender)

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


@csrf_exempt
def add_comment(request, pk):
    if request.method == 'POST':
        req_token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = Token.objects.get(key=req_token)

        if not token:
            return HttpResponseRedirect(reverse('inbox'))
        else:
            input = Input.objects.get(pk=pk)
            user = User.objects.get(pk=request.POST['user_id'])
            comment = Comment.objects.create(input=input, text=request.POST['text'], user=user)
            return JsonResponse({'message': "Comment has been added."})
    else: 
        return HttpResponseRedirect(reverse('album:detail', args=[pk]))

