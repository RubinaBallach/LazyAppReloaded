from rest_framework import serializers
from .models import LazyUser, LazyUserManager

class LazyUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user_id', read_only=True)

    class Meta:
        model = LazyUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'created_at',
            'last_login',
            'is_active'
        ]

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = LazyUser
        fields = "__all__"

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if LazyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = LazyUser.objects.create_user(password=password, **validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LazyUser
        fields = ('first_name', 'last_name', 'email', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance
