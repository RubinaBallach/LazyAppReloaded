from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..users.serializers import LazyUserSerializer

# from rest_framework import serializers
# from .models import CustomUser


#lazyreload/apps/users/serializers.py


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str. Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        # get the tokens (both access and refresh token)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh) # refresh token
        data['access'] = str(refresh.access_token) # access token


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user