from django.db import models
from .manager import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin




class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'), 
        ('PATIENT', 'Patient'), 
        ('DOCTOR', 'Doctor'),)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='PATIENT')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0)
    mobile = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    objects = UserManager()

    def __str__(self):
        return self.mobile




