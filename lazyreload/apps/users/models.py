from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid



# Create your models here.

class LazyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password):
        if email is None:
            raise TypeError("Please enter an email address.")
        if username is None:
            raise TypeError("Please enter a username.")
        if password is None:
            raise TypeError
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class LazyUser(AbstractBaseUser):
    user_id = models.UUIDField(
        db_index=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
        ) # index to increase speed
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=True)
    created_at = models.DateTimeField(verbose_name="signed up", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

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
    

