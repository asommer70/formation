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
        from pyquery import PyQuery as pq
        if not self.pk:
            content = pq(self.content)
            # print('content(input).name:', content('input').attr('name'))
            inputs = content('input')
            print('inputs:', inputs)
            for input in inputs:
                input = pq(input)
                if not input.attr(':value'):
                    print('input.attr(:value):', input.attr(':value'))
                    input.attr(':value', 'this.input.' + input.attr('name'))
                    print('input:', input.html())

        super(Form, self).save(*args, **kwargs)
