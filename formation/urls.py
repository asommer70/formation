from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import IndexView


urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('forms/', include('forms.urls', namespace='forms')),
    path('inbox/', include('inputs.urls', namespace='inbox')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
    path('', IndexView.as_view()),
]
