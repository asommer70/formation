from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from inputs.models import Input
from forms.models import Form
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

    def test_create(self):
        self.assertEqual(self.input.status, 'new')
        self.assertEqual(self.input.user.username, 'test')

    def test_route_model(self):
        self.input.status = 'routed'
        self.input.route_holder = self.group.user_set.last()
        self.input.route_sender = self.user
        self.input.save()

        self.assertEqual(self.input.route_holder.username, 'other')
        self.assertEqual(self.input.status, 'routed')

    def test_api_input_update(self):
        url = reverse('api:input', kwargs={'pk': self.input.pk})
        request = self.factory.patch(url, {
            'status': 'routed',
            'route_holder': self.group.user_set.last().id,
            'route_sender': self.user.id,
        })
        force_authenticate(
            request,
            user=self.user,
            token=self.user.auth_token
        )

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
