from django.urls import path
from .views import LazyJobApplicationView

urlpatterns = [
    path('create-job-application/', LazyJobApplicationView.as_view(), name="create-job-application"),
]