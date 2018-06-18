from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group
from forms.models import Form
from routes.models import Route


User = get_user_model()


class RouteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='testers',
            email='test@thehoick.com'
        )
        self.group = Group.objects.create(name="IT Dept")
        self.user.groups.add(self.group)

        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html'
        )

        self.route = Route.objects.create(
            form=self.form,
            user=self.user,
            group=self.group
        )

    def test_create(self):
        self.assertEqual(self.route.form.name, 'Test Form')
        self.assertEqual(self.route.user.username, 'test')

    def test_update(self):
        accounting = Group.objects.create(name='Accounting')
        self.route.group = accounting
        self.route.save()

        route = Route.objects.get(pk=self.route.pk)

        self.assertEqual(route.group.name, 'Accounting')

    def test_delete(self):
        self.assertEqual(Route.objects.all().count(), 1)
        self.route.delete()
        self.assertEqual(Route.objects.all().count(), 0)

