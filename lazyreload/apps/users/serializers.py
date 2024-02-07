from rest_framework import serializers
from .models import LazyUser

class LazyUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user_id', read_only=True)

    class Meta:
        model = LazyUser
        fields(
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'created_at',
            'last_login',
            'is_active'
        )