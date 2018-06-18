from django.urls import path
from . import views


app_name = 'routes'
urlpatterns = [
    path('', views.RouteListView.as_view(), name='list'),
    path('create', views.RouteCreateView.as_view(), name='create'),
    path('<int:pk>', views.RouteDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.RouteUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.RouteDeleteView.as_view(), name='delete'),
]
