from rest_framework import serializers
from .models import LazyUser, LazyUserProfile
from rest_framework.validators import UniqueValidator
from django.core.validators import (
    EmailValidator,
    RegexValidator,
    FileExtensionValidator,
)
from django.utils.timezone import now


class CapitalizeNameField(serializers.CharField):
    def __call__(self, value):
        return value.title()


# class LoginSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs: Dict[str. Any]) -> Dict[str, str]:
#         data = super().validate(attrs)
#         # get the tokens (both access and refresh token)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh) # refresh token
#         data['access'] = str(refresh.access_token) # access token


class LazyUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="user_id", read_only=True)
    username = serializers.SlugField(
        max_length=60,
        validators=[
            UniqueValidator(
                queryset=LazyUser.objects.all(), message="Username already exists."
            ),
            RegexValidator(r"^\w+$", message="Username cannot contain profanities"),
        ],
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            EmailValidator(message="Invalid email address"),
        ],
    )
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def to_representation(self, instance):
        instance.first_name = CapitalizeNameField()(instance.first_name)
        instance.last_name = CapitalizeNameField()(instance.last_name)
        return super().to_representation(instance)

    def create(self, validated_data):
        user = LazyUser(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, validated_data):
        user = LazyUser(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = LazyUser
        fields = [
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
        ]


class LazyUserProfileSerializer(serializers.ModelSerializer):
    use_case = serializers.CharField(max_length=60, required=True)
    if use_case == "job" or "both":
        cv_file = serializers.FileField(
            required=True,
            validators=[
                FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])
            ],
        )
    else:
        cv_file = serializers.FileField(required=False)

    email = serializers.EmailField(
        default=LazyUser.email,
        validators=[
            EmailValidator(message="Invalid email address"),
        ],
    )
    availability = serializers.DateTimeField(default=now)

    class Meta:
        model = LazyUserProfile
        fields = ["use_case", "cv_file", "email"]
