from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
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

# User Authendication MOdel
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


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug=models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering=('name',)
        verbose_name ='category'
        verbose_name_plural='categories'                                              

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('shop:product_list_by_category', args=[self.slug])


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    b_description = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    slug=models.SlugField(max_length=200,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together=(('id','slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pure:product_detail', args=[self.slug])
