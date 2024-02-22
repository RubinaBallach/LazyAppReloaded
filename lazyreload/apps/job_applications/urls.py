from django.urls import path
from .views import LazyJobApplicationAPIView

urlpatterns = [
    path('create-job-application/', LazyJobApplicationAPIView.as_view(), name="create-job-application"),
]