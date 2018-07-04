from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from forms.models import Form
from routes.models import Route, Destination


User = get_user_model()


class Input(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=255, default="new")
    data = JSONField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, default=None)

    route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True
    )
    route_date = models.DateTimeField(blank=True, null=True)
    route_holder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name='user_holding_input'
    )
    route_sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name='user_sent_input'
    )
    current_dest = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
    step = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username + ": " + self.status


class Approval(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    input = models.ForeignKey(Input, on_delete=models.DO_NOTHING, default=None)

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    input = models.ForeignKey(Input, on_delete=models.DO_NOTHING, default=None)
    text = models.CharField(max_length=2048)

    class Meta:
        ordering = ['-created_at']
