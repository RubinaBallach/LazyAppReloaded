from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LazyUser, LazyUserProfile

# Register your models here.

admin.site.register(LazyUser, UserAdmin) # registered custom user model
admin.site.register(LazyUserProfile) # registered custom user profile model