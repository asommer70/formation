from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse


User = get_user_model()


class Form(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(max_length=20000, blank=True, null=True)
    fields = JSONField(blank=True, null=True)
    public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forms:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        from bs4 import BeautifulSoup
        # Make sure inputs, textareas, and selects have bound Vue attributes.
        soup = BeautifulSoup(self.content, 'html.parser')

        fields = {}
        for input in soup.find_all('input'):
            fields[input['name']] = ""
            # input_types = ['text', 'tel', 'number', 'email', 'url']
            if not 'v-model' in input:
                input['v-model'] = input['name']
            if not '@blur' in input:
                input['@blur'] = 'saveInput'

        #     if input['type'] == 'checkbox' and not ':checked' in input:
        #         input[':checked'] = 'this.input.' + input['name']
        #     if input['type'] == 'checkbox' and not '@blur' in input:
        #         input['@blur'] = 'saveInput'

        #     if input['type'] == 'radio' and not 'v-model' in input:
        #         input['v-model'] = 'this.input.' + input['name']
        #     if input['type'] == 'radio' and not '@blur' in input:
        #         input['@blur'] = 'saveInput'

        for textarea in soup.find_all('textarea'):
            fields[textarea['name']] = ""
            if not 'v-model' in textarea:
                textarea['v-model'] = textarea['name']
            if not '@blur' in textarea:
                textarea['@blur'] = 'saveInput'

        for select in soup.find_all('select'):
            fields[select['name']] = ""
            if not 'v-model' in select:
                select['v-model'] = select['name']
            if not '@blur' in select:
                select['@blur'] = 'saveInput'

        self.fields = fields
        self.content = soup.prettify()
        super(Form, self).save(*args, **kwargs)
