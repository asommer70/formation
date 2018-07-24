from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()


class Form(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(max_length=20000, blank=True, null=True)
    fields = JSONField(blank=True, null=True)
    public = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to='form_images')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forms:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        from bs4 import BeautifulSoup
        # Make sure inputs, textareas, and selects have bound Vue attributes.
        fields = {}

        if self.content:
            soup = BeautifulSoup(self.content, 'html.parser')

            # Add a v-model and @blur attribute to all inputs, textareas,
            # and selects.
            for input in soup.find_all('input'):
                fields[input['name']] = ""
                if 'v-model' not in input:
                    input['v-model'] = input['name']
                if '@blur' not in input:
                    input['@blur'] = 'saveInput'

            for textarea in soup.find_all('textarea'):
                fields[textarea['name']] = ""
                if 'v-model' not in textarea:
                    textarea['v-model'] = textarea['name']
                if '@blur' not in textarea:
                    textarea['@blur'] = 'saveInput'

            for select in soup.find_all('select'):
                fields[select['name']] = ""
                if 'v-model' not in select:
                    select['v-model'] = select['name']
                if '@blur' not in select:
                    select['@blur'] = 'saveInput'

        self.fields = fields
        self.content = soup.prettify()
        super(Form, self).save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
