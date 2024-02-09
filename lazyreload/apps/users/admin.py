from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LazyUser

# Register your models here.

admin.site.register(LazyUser, UserAdmin) # registered custom user model