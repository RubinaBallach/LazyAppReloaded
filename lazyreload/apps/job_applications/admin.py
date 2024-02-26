from django.contrib import admin
from .models import Company, LazyJobApplication

# Register your models here.

admin.register(Company)
admin.register(LazyJobApplication)