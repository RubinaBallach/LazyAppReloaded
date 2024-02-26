from django.urls import path
from .views import LazyJobApplicationAPIView

app_name = 'job_applications'
urlpatterns = [
    path('api/create-job-application/', LazyJobApplicationAPIView.as_view(), name="create-job-application"),
]