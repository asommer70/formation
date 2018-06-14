from django.contrib.auth import get_user_model
from django.test import TestCase
from forms.models import Form


User = get_user_model()


class FormTestCase(TestCase):
    def setUp(self):
        content = """
          <input type="text" name="test" />
          <br/>
          <input type="text" name="beans" />
        """
        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html',
            content=content
        )

    def test_create(self):
        self.assertEqual(self.form.name, 'Test Form')
        self.assertFalse(self.form.public)
        self.assertTrue(':value' in self.form.content)

    def test_update(self):
        self.form.public = True
        self.form.save()

        self.assertTrue(self.form.public)

    def test_delete(self):
        self.assertEqual(Form.objects.all().count(), 1)
        self.form.delete()
        self.assertEqual(Form.objects.all().count(), 0)
