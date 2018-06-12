from django.urls import path
from . import views


app_name = 'inbox'
urlpatterns = [
    path('', views.InputListView.as_view(), name='list'),
    path('create', views.InputCreateView.as_view(), name='create'),
    # path('<int:pk>', views.FormDetailView.as_view(), name='detail'),
    # path('<int:pk>/edit', views.FormUpdateView.as_view(), name='update'),
    # path('<int:pk>/edit', views.PropertyUpdateView.as_view(), name='update'),
    # path('<int:pk>/delete', views.FormDeleteView.as_view(), name='delete'),
]
