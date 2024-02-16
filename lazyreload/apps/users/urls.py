from django.urls import path
from .views import CreateUserAPI, LazyUpdateUserAPIView, UserListView, LoginView, LazyUserProfileView



urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('update-user/<str:username>/', LazyUpdateUserAPIView.as_view(), name='update-user'),
    path('users-list/', UserListView.as_view(), name='list-users'),
    path('user-profile/', LazyUserProfileView.as_view(), name = 'user-profile'),
    path('login/', LoginView.as_view(), name="login")
  
]