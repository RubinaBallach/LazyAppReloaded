from django.urls import path
from .views import ( CreateUserAPI, LazyUpdateUserAPIView, UserListView, 
                    LoginView, LazyUserProfileView, LazyDeleteUserAPIView,
                    HomeView, AboutUsView, ContactView)

app_name = 'users'

urlpatterns = [

    path('register/', CreateUserAPI.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('users-list/', UserListView.as_view(), name='list-users'),
    path('userprofile/<uuid:user_id>/', LazyUserProfileView.as_view(), name = 'userprofile'),
    path('update-user/<uuid:user_id>/', LazyUpdateUserAPIView.as_view(), name='update-user'),
    path('delete-user/<uuid:user_id>/', LazyDeleteUserAPIView.as_view(), name='delete-user'),
    path('home/',HomeView.as_view(), name='home'),
    path('aboutus/',AboutUsView.as_view(), name='aboutus'),
    path('contact/',ContactView.as_view(), name='contact')
]

