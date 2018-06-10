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
    public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forms:detail', kwargs={'pk': self.pk})


class Input(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=255, default="new")
    data = JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    route_date = models.DateTimeField(blank=True, null=True)
    # route_holder = User
    # route_sender = User
    # route = Route
    # approvals = User
    # attachments
    # comments = Comment

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username + ": " + self.status
