from django.urls import path
from . import views


app_name = 'forms'
urlpatterns = [
    path('', views.FormListView.as_view(), name='list'),
]
