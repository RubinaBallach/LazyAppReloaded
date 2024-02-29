from django.urls import path
from .views import LazyJobApplicationAPIView, LazyJobApplicationDashboardAPIView, CompanyAPIView

app_name = 'job_applications'
urlpatterns = [
    path('api/job-application/', LazyJobApplicationAPIView.as_view(), name="job-application"),
    path('api/job-application-dashboard/', LazyJobApplicationDashboardAPIView.as_view(), name="job-application-dashboard"),
    path('api/company/', CompanyAPIView.as_view(), name='company'),
]