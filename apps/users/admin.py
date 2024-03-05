from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LazyUser, LazyUserProfile

# Register your models here.
@admin.register(LazyUser)
class LazyUserAdmin(admin.ModelAdmin):
    fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['user_id', 'is_superuser']

@admin.register(LazyUserProfile)
class LazyUserProfileAdmin(admin.ModelAdmin):
    fields = ['lazy_user_id', 'user', 'use_case', 'cv_file', 'cv_text', 'email', 'availability']
    readonly_fields = ['lazy_user_id', 'user', 'cv_text']
