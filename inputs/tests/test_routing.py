from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.functions import Now
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from inputs.models import Input
from forms.models import Form
from routes.models import Route, Destination
from api import views
import json

User = get_user_model()


class RoutingTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create(
            username='test',
            password='testers',
            email='test@thehoick.com'
        )
        self.token = Token.objects.create(user=self.user)

        self.other_user = User.objects.create(
            username='other',
            password='others',
            email='other@thehoick.com'
        )
        self.other_token = Token.objects.create(user=self.other_user)

        self.group = Group.objects.create(name="IT Dept")
        self.user.groups.add(self.group)
        self.other_user.groups.add(self.group)

        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html',
            content='<input type="text" name="tester"/>'
        )

        self.input = Input.objects.create(
            status='new',
            data={"test": "yes please...", "more": True},
            user=self.user,
            form=self.form
        )

        self.route = Route.objects.create(
            form=self.form,
            user=self.user,
            group=self.group
        )

        self.destination = Destination.objects.create(
            route=self.route,
            user=self.user,
            step=0,
            name='Start'
        )

        self.destination = Destination.objects.create(
            route=self.route,
            group_id=self.group.id,
            step=1,
            name='Destination 1'
        )

    def test_create(self):
        self.assertEqual(self.input.status, 'new')
        self.assertEqual(self.input.user.username, 'test')
        self.assertEqual(self.route.destination_set.count(), 2)

    def test_route(self):
        self.input.status = 'routed'
        self.input.route = self.route
        self.input.route_date = Now()
        self.input.route_holder = self.group.user_set.last()
        self.input.route_sender = self.user
        self.input.current_dest = Destination.objects.filter(
            route=self.route,
            step=1
        ).first()
        self.input.step = self.input.current_dest.step
        self.input.save()

        self.assertEqual(self.input.step, 1)
        self.assertEqual(self.input.route_holder.username, 'other')
        self.assertEqual(self.input.status, 'routed')

    def test_api_input_update(self):
        url = reverse('api:input', kwargs={'pk': self.input.pk})
        request = self.factory.patch(url, {
            'status': 'routed',
            'route_id': self.route.id,
            'route_date': Now(),
            'route_holder': self.group.user_set.last().id,
            'route_sender': self.user.id,
            'current_dest_id':  Destination.objects.filter(
                                    route=self.route,
                                    step=1
                                ).first().id,
            'step': 1
        })
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        force_authenticate(request, user=self.user, token=self.user.auth_token)

        response = views.RetrieveUpdateDestroyInput.as_view()(request,
                                                              pk=self.input.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'],
                         'Input successfully updated.')

        req_2 = self.factory.get(url)
        force_authenticate(req_2, user=self.user, token=self.user.auth_token)

        res_2 = views.RetrieveUpdateDestroyInput.as_view()(req_2,
                                                           pk=self.input.pk)
        res_2.render()

        self.assertEqual(res_2.status_code, 200)
        self.assertEqual(json.loads(res_2.content)['status'],
                         'routed')
