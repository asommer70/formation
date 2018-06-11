from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from forms.models import Form


User = get_user_model()


class Input(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=255, default="new")
    data = JSONField()
    route_date = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, default=None)
    # route_holder = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    # route_sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    # route = models.ForeignKey(Route, on_delete=models.CASCADE, default=None)

    # approvals = User
    # attachments
    # comments = Comment

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username + ": " + self.status
