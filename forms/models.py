from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse


User = get_user_model()


class Form(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(max_length=20000, blank=True, null=True)
    public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forms:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(self.content, 'html.parser')

        for input in soup.find_all('input'):
            if input['type'] == 'text' and not ':value' in input:
                input[':value'] = 'this.input.' + input['name']
            if (input['type'] == 'checkbox' or input['type'] == 'radio') and not ':checked' in input:
                input[':checked'] = 'this.input.' + input['name']
                
        for textarea in soup.find_all('textarea'):
            if not ':value' in textarea:
                textarea[':value'] = 'this.input.' + textarea['name']
                
        self.content = soup.prettify()
        super(Form, self).save(*args, **kwargs)
