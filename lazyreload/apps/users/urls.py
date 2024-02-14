from django.urls import path
from .views import CreateUserAPI, UpdateUserAPI, UserListView



urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('update-user/<int:pk>/', UpdateUserAPI.as_view()),
    path('users-list/', UserListView.as_view(), name='list-users'),
  
]