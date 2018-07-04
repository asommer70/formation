from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from forms.models import Form


User = get_user_model()


class FormViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html',
            content='<input name="test" type="text"/>'
        )

        self.user = User.objects.create(
            username="tester",
            email="tester@thehoick.com",
            password="tests",
            is_staff=True
        )

    def test_list_unauthenticated(self):
        login_url = '/accounts/login'
        response = self.client.get(reverse('forms:list'), follow=True)
        self.assertRedirects(response, login_url + '/?next=/forms/')

    def test_list_authenticated(self):
        url = reverse('forms:list')
        self.client.force_login(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['forms'].count(), 1)

    def test_form_create(self):
        url = reverse('forms:create')
        self.client.force_login(user=self.user)

        response = self.client.post(url, {
            'name': 'Test POST Form',
            'content': '<input type="text" name="tester"/>'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/forms/')
        self.assertEqual(Form.objects.all().count(), 2)

    def test_form_detail(self):
        url = reverse('forms:detail', kwargs={'pk': self.form.pk})
        self.client.force_login(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].public, False)

    def test_form_update(self):
        url = reverse('forms:update', kwargs={'pk': self.form.pk})
        self.client.force_login(user=self.user)

        response = self.client.post(url, {
            'public': True,
            'content': '<input type="text" name="tester"/>'
        })
        form = Form.objects.get(pk=self.form.pk)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/forms/{}'.format(form.pk))
        self.assertEqual(form.public, True)

    def test_form_delete(self):
        url = reverse('forms:delete', kwargs={'pk': self.form.pk})
        self.client.force_login(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms/form_confirm_delete.html')
