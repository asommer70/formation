from django.contrib.auth import get_user_model
from django.test import TestCase
from inputs.models import Input
from forms.models import Form


User = get_user_model()


class InputTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='testers',
            email='test@thehoick.com'
        )

        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html'
        )

        self.input = Input.objects.create(
            status='new',
            data={"things": "yes please...", "more": True},
            user=self.user,
            form=self.form
        )

    def test_create(self):
        self.assertEqual(self.input.status, 'new')
        self.assertEqual(self.input.user.username, 'test')

    def test_update(self):
        self.input.status = 'routed'
        self.input.save()

        input = Input.objects.get(pk=self.input.pk)

        self.assertEqual(input.status, 'routed')

    def test_delete(self):
        self.assertEqual(Input.objects.all().count(), 1)
        self.input.delete()
        self.assertEqual(Input.objects.all().count(), 0)
