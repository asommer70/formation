from django.urls import path
from . import views


app_name = 'forms'
urlpatterns = [
    path('', views.FormListView.as_view(), name='list'),
    path('create', views.FormCreateView.as_view(), name='create'),
    path('<int:pk>', views.FormDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.FormUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.FormDeleteView.as_view(), name='delete'),
]
