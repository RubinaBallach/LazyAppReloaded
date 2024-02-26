from django.urls import path
from .views import CreateUserAPI, LazyUpdateUserAPIView, UserListView, LoginView, LazyUserProfileView, LazyDeleteUserAPIView

app_name = 'users'

urlpatterns = [
    path('api/create-user/', CreateUserAPI.as_view()),
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/users-list/', UserListView.as_view(), name='list-users'),
    path('api/user-profile/', LazyUserProfileView.as_view(), name = 'user-profile'),
    path('api/update-user/<uuid:user_id>/', LazyUpdateUserAPIView.as_view(), name='update-user'),
    path('api/delete-user/<uuid:user_id>/', LazyDeleteUserAPIView.as_view(), name='delete-user'),   
]