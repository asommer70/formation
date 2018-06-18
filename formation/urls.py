from django.contrib import admin
# from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import IndexView


urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('forms/', include('forms.urls', namespace='forms')),
    path('inbox/', include('inputs.urls', namespace='inbox')),
    path('routes/', include('routes.urls', namespace='routes')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', IndexView.as_view()),
]
