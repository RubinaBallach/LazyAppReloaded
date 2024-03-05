from rest_framework import serializers
from .models import LazyUser, LazyUserProfile
from rest_framework.validators import UniqueValidator
from django.core.validators import (
    EmailValidator,
    RegexValidator,
    FileExtensionValidator,
)
from django.utils.timezone import now
from apps.core.utils import CVTextExtractor
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



class CapitalizeNameField(serializers.CharField):
    def __call__(self, value):
        return value.title()



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


class LazyLoginSerializer(serializers.Serializer):

    username = serializers.CharField(required= False)
    password = serializers.CharField(write_only=True, required=False)


class LazyUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LazyUser
        fields = ['email', 'username', 'first_name', 'last_name']


class LazyUserProfileSerializer(serializers.ModelSerializer):
    lazy_user_id = serializers.UUIDField(source="user.user_id", read_only=True)
    use_case = serializers.CharField(max_length=60, required=True)
    cv_file = serializers.FileField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])]
    )
    email = serializers.EmailField(
        default=LazyUser.email,
        validators=[EmailValidator(message="Invalid email address")]
    )

    def create(self, validated_data):
        cv_text_generator = CVTextExtractor(
            OPENAI_API_KEY,
            file_path=validated_data["cv_file"],
        )
        cv_text = cv_text_generator.extract_cv_info()
        user_profile = LazyUserProfile(
            use_case=validated_data["use_case"],
            cv_file=validated_data["cv_file"],
            cv_text=cv_text,
            email=validated_data["email"],

        )
        user_profile.save()
        return user_profile

    class Meta:
        model = LazyUserProfile
        fields = ["use_case", "cv_file", "email", "cv_text", "lazy_user_id"]