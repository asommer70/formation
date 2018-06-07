from django.contrib import admin
from django.urls import path, include
from .views import IndexView


urlpatterns = [
    path('forms/', include('forms.urls', namespace='forms')),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
]
