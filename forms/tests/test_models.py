from django.test import TestCase
from forms.models import Form


class FormTestCase(TestCase):
    def setUp(self):
        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html'
        )

    def test_create(self):
        self.assertEqual(self.form.name, 'Test Form')
        self.assertFalse(self.form.public)

    def test_update(self):
        self.form.public = True
        self.form.save()

        self.assertTrue(self.form.public)

    def test_delete(self):
        self.assertEqual(Form.objects.all().count(), 1)
        self.form.delete()
        self.assertEqual(Form.objects.all().count(), 0)










