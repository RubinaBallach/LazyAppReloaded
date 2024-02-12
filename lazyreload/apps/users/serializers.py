from rest_framework import serializers
from .models import LazyUser, LazyUserProfile
from validate_email import validate_email


def email_validation(value):
    '''performs advanced email validation using the validate_email library
    - correct format using regex
    - costum error message
    - check if host has SMTP server and the email really exists'''
    if not validate_email(value, verify=True):
        raise serializers.ValidationError("Invalid email format.")
    return value

    

class LazyUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user_id', read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[email_validation]
        )

    class Meta:
        model = LazyUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_active'
        ]

class LazyUserProfileSerializer(serializers.ModelSerializer):
    pass