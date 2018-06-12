from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'api'
urlpatterns = [
    path('forms/', views.ListCreateForm.as_view(), name="forms"),
    path('forms/<int:pk>', views.RetrieveUpdateDestroyForm.as_view(), name="forms"),

    path('inbox/', views.ListCreateInput.as_view(), name="inbox"),
    path('inbox/<int:pk>', views.RetrieveUpdateDestroyInput.as_view(), name="input")
]
