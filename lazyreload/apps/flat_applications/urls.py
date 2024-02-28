# project/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lazyreload/', include('lazyreload.urls')),  # Replace with the correct app name
    # Add more app URLs as needed
]
