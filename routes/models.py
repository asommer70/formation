from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from forms.models import Form


User = get_user_model()


class Route(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forms:detail', kwargs={'pk': self.pk})


class Destination(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
    step = models.IntegerField(default=1)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return "self.id: {}, route.id: {}, step: {}, user: {}, group: {}, created_at: {}".format(
            self.id,
            self.route,
            self.step,
            self.user,
            self.group,
            self.created_at
        )

    def save(self, *args, **kwargs):
        print('Destination save() args:', args, 'kwargs:', kwargs)
        super(Destination, self).save(*args, **kwargs)
        print('self:', self)
