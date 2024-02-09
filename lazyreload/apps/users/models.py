from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid



# Create your models here.

class LazyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            email,
            username,
            first_name,
            last_name,
            password,
            **extra_fields
        )

class LazyUser(AbstractBaseUser):
    user_id = models.UUIDField(
        db_index=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
        ) # index to increase speed
    objects = LazyUserManager()
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    created_at = models.DateTimeField(verbose_name="signed up", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    

    USE_CASE_CHOICES = (
        ("Job Applications", "Job Applications"),
        ("Flat Applications", "Flat Applications"),
        ("Job&Flat Applications", "Job&Flat Applications")
    )
    use_case = models.CharField(max_length=60, choices=USE_CASE_CHOICES, default="Job&Flat Applications")

    # for login with username and password
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username + "," + self.email
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    

