from rest_framework import serializers
from .models import LazyUser, LazyUserProfile
from rest_framework.validators import UniqueValidator
from django.core.validators import EmailValidator,RegexValidator


# #class CapitalizeNameField(serializers.CharField):
#     def __call__(self, value):
#         return value.title()
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


class LazyUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='user_id', read_only=True)
    username = serializers.SlugField(
        max_length=60,
        validators=[
            UniqueValidator(queryset=LazyUser.objects.all(), message="Username already exists."),
            RegexValidator(r'^\w+$', message='Username cannot contain profanities'),
            ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator(message="Invalid email address"),]
        )

    # #def to_internal_value(self, data):
    #     data['first_name'] = CapitalizeNameField(data['first_name'])
    #     data['last_name'] = CapitalizeNameField(data['last_name'])
    #     return super().to_internal_value(data)
    
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
    cv_file = serializers.FileField()
    