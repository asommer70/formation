from django.db.models import Q
from django import template
from inputs.models import Input

register = template.Library()


@register.filter(name='inbox_count')
def inbox_count(user):
    return Input.objects.filter(
        Q(user=user) | Q(route_holder=user)
    ).exclude(status='archived').count()
