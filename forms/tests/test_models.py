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
          <br/>
          <input type="number" name="size" />
          <br/>
          <textarea name="desc"></textarea>
          <br/>
          <input type="checkbox" name="tacos" />
          <input name="yes_or_no" type="radio" value="no" />
          <input name="yes_or_no" type="radio" value="yes" />
          <br/>
          <select id="selector" name="selector">
           <option value="first">
            First Value
           </option>
           <option selected="" value="second">
            Second Value
           </option>
           <option value="third">
            Third Value
           </option>
          </select>
        """
        self.form = Form.objects.create(
            name='Test Form',
            path='media/forms/test_form.html',
            content=content
        )

    def test_create(self):
        self.assertEqual(self.form.name, 'Test Form')
        self.assertFalse(self.form.public)
        self.assertTrue('v-model' in self.form.content)
        self.assertEqual(self.form.content.count('v-model'), 2)

    def test_update(self):
        self.form.public = True
        self.form.save()

        self.assertTrue(self.form.public)

    def test_delete(self):
        self.assertEqual(Form.objects.all().count(), 1)
        self.form.delete()
        self.assertEqual(Form.objects.all().count(), 0)
