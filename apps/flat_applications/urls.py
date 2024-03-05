from django.contrib import admin
from django.urls import include, path
from .views import LazyFlatApplicationAPIView, LazyRenterAPIView, LandlordAPIView

app_name = 'flat_applications'
urlpatterns = [
    path('api/lazyrenter-profile/', LazyRenterAPIView.as_view(), name='lazyrenter-profile'),
    path('api/flat-application/', LazyFlatApplicationAPIView.as_view(), name='flat-application'), 
    path('api/landlord/', LandlordAPIView.as_view(), name='landlord'),
    # Add more app URLs as needed
]
