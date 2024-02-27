from django.contrib import admin
from .models import Company, LazyJobApplication

# Register your models here.

admin.site.register(Company)
admin.site.register(LazyJobApplication)