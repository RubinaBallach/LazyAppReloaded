from django.urls import path
from .views import CreateUserAPI, UpdateUserAPI



urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('update-user/<int:pk>/', UpdateUserAPI.as_view()),
  
]