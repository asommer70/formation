from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group
from forms.models import Form
from routes.models import Route, Destination


User = get_user_model()


class RouteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='testers',
            email='test@thehoick.com'
        )

        self.other = User.objects.create(
            username='other',
            password='others',
            email='other@thehoick.com'
        )

        self.group = Group.objects.create(name="IT Dept")
        self.user.groups.add(self.group)

        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html',
            content='<input type="text" name="tester"/>'
        )

        self.route = Route.objects.create(
            form=self.form,
            user=self.user,
            group=self.group
        )

        self.destination = Destination.objects.create(
            route=self.route,
            user=self.user
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

    def test_create_destination(self):
        self.assertEqual(self.destination.user.username, 'test')
        self.assertEqual(self.destination.route.group.name, 'IT Dept')
        self.assertEqual(self.destination.route.form.name, 'Test Form')
        self.assertEqual(
            self.form.route_set.first().destination_set.first().user.username,
            'test'
        )

    def test_update_destination(self):
        self.destination.user = self.other
        self.destination.save()

        dest = Destination.objects.get(pk=self.destination.pk)

        self.assertEqual(dest.user.username, 'other')

    def test_delete_destination(self):
        self.assertEqual(Destination.objects.all().count(), 1)
        self.destination.delete()
        self.assertEqual(Destination.objects.all().count(), 0)
