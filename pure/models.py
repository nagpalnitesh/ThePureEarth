from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# User model
class Profile(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default='Guest')
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    session_token = models.CharField(max_length=10, default=0)
    profile_auth_token = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=50, null=True, blank=True)
    forget_password_token = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_Verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username