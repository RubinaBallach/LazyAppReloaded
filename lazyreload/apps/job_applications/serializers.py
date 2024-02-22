from rest_framework import serializers
from .models import LazyJobApplication, Company
from apps.users.models import LazyUserProfile, LazyUser

class LazyJobApplicationSerializer(serializers.Serializer):
    pass


class CompanySerializer(serializers.Serializer):
    pass