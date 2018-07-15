from django.urls import path
from . import views


app_name = 'inbox'
urlpatterns = [
    path('', views.InputListView.as_view(), name='list'),
    path('create', views.InputCreateView.as_view(), name='create'),
    path('<int:pk>', views.InputDetailView.as_view(), name='detail'),
    path('<int:pk>/delete', views.InputDeleteView.as_view(), name='delete'),
    path('archive', views.ArchiveListView.as_view(), name='archive'),
]
