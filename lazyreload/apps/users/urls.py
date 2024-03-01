from django.urls import path
from .views import ( CreateUserAPI, LazyUpdateUserAPIView, UserListView, 
                    LoginView, LazyUserProfileView, LazyDeleteUserAPIView,
                    HomeView)

app_name = 'users'

urlpatterns = [
    path('api/create-user/', CreateUserAPI.as_view(), name='create-user'),
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/users-list/', UserListView.as_view(), name='list-users'),
    path('api/user-profile/<uuid:user_id>/', LazyUserProfileView.as_view(), name='user-profile'),
    path('api/update-user/<uuid:user_id>/', LazyUpdateUserAPIView.as_view(), name='update-user'),
    path('api/delete-user/<uuid:user_id>/', LazyDeleteUserAPIView.as_view(), name='delete-user'),   
    path('home/',HomeView.as_view(), name='home')
]
