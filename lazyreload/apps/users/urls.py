from django.urls import path
from .views import CreateUserAPI, LazyUpdateUserAPIView, UserListView, LoginView, LazyUserProfileView, LazyDeleteUserAPIView


urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('login/', LoginView.as_view(), name="login"),
    path('users-list/', UserListView.as_view(), name='list-users'),
    path('user-profile/', LazyUserProfileView.as_view(), name = 'user-profile'),
    path('update-user/<uuid:user_id>/', LazyUpdateUserAPIView.as_view(), name='update-user'),
    path('delete-user/<uuid:user_id>/', LazyDeleteUserAPIView.as_view(), name='delete-user'),
    
  
]