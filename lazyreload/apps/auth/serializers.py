from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..user.serializers import LazyUserSerializer

#lazyreload/apps/users/serializers.py


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str. Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        # get the tokens (both access and refresh token)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh) # refresh token
        data['access'] = str(refresh.access_token) # access token