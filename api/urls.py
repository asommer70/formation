from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'api'
urlpatterns = [
    path('forms/', views.ListCreateForm.as_view(), name="forms"),
    path('forms/<int:pk>', views.RetrieveUpdateDestroyForm.as_view(), name="del_form"),

    path('inbox/', views.ListCreateInput.as_view(), name="inbox"),
    path('inbox/<int:pk>', views.RetrieveUpdateDestroyInput.as_view(), name="input"),

    path('users/', views.ListCreateUser.as_view(), name="users"),
    path('groups/', views.ListCreateGroup.as_view(), name="groups"),

    path('routes/', views.ListCreateRoute.as_view(), name="routes"),
    path('destinations/', views.ListCreateDestination.as_view(), name="destinations"),
    path('destinations/<int:pk>', views.RetrieveUpdateDestroyDestination.as_view(), name="del_dest"),
]
