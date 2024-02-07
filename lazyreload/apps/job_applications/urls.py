from django.urls import path
from .views import LazyJobApplicationAPIView # LazyJobApplicationDetailView

app_name = 'job_applications'
urlpatterns = [
    path('api/create-job-application/', LazyJobApplicationAPIView.as_view(), name="create-job-application"),
    # path('applications/<int:pk>', LazyJobApplicationDetailView.as_view(), name="application-detail"),
]