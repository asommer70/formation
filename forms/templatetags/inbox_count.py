from django import template
from inputs.models import Input

register = template.Library()


@register.filter(name='inbox_count')
def inbox_count(user):
    return Input.objects.filter(user=user).count()
