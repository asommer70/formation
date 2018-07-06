from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
import json
from . import views
from forms.models import Form

User = get_user_model()


class ApiTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="tester",
            email="tester@blueridgevacationcabins.com",
            password="tests",
            is_staff=True
        )
        self.token = Token.objects.create(user=self.user)

        self.group = Group.objects.create(name="IT Dept")
        self.user.groups.add(self.group)

        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html',
            content='<input type="text" name="tester"/>'
        )

    def test_forms_list(self):
        url = reverse('api:forms')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.user.auth_token)

        response = views.ListCreateForm.as_view()(request)
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[0]['name'],
                         self.form.name)
