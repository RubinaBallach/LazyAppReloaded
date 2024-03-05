from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.timezone import now
import uuid


class LazyUserManager(UserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class LazyUser(AbstractUser):
    user_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )  # index to increase speed
    objects = LazyUserManager()
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # for login with username and password
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class LazyUserProfile(models.Model):
    lazy_user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        LazyUser, on_delete=models.CASCADE, related_name="profile"
    )
    USE_CASE_CHOICES = [
        ("job", "Job Applications"),
        ("flat", "Flat Applications"),
        ("both", "Job&Flat Applications"),
    ]
    use_case = models.CharField(max_length=60, choices=USE_CASE_CHOICES, default="job")
    cv_file = models.FileField(upload_to="cvs", blank=True, null=True)
    cv_text = models.TextField(blank=True, null=True)
    email = models.EmailField(
        max_length=60, blank=True
    )  # user might want to use a different mailadress for applications that for lazyapp signup
    availability = models.DateField(verbose_name="Earliest Start Date")

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.user.email
        if not self.availability:
            self.availability = now()
        super(LazyUserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
