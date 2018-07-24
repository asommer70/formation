from django.contrib import admin
from .models import Input, Approval, Attachment, Comment


admin.site.register(Input)
admin.site.register(Approval)
admin.site.register(Attachment)
admin.site.register(Comment)
