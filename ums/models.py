from django.db import models
from tour.models import Destination,Hotel, Airline
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



# class Guest(AbstractBaseUser):
#     username = models.CharField(max_length=200, null=True)
#     phone = models.CharField(max_length=200, null=True)
#     email = models.EmailField(max_length=200,unique=True)
#     country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
#     arrival_date = models.DateField(null=True)
#     departure_date = models.DateField(null=True)
#     destination = models.ForeignKey(Destination, null=True, on_delete=models.SET_NULL)
#     hotel = models.ForeignKey(Hotel, null=True, on_delete=models.SET_NULL)
#     airline = models.ForeignKey(Airline, null=True, on_delete=models.SET_NULL)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     first_name = models.CharField(max_length=200, null=True)
#     last_name= models.CharField(max_length=200, null=True)
#     USERNAME_FIELD = 'email'
#     password = models.CharField(max_length=20)
    
#     def __str__(self):
#         return self.username


class GuestManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True) 
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = GuestManager()
    
    def __str__(self):
        return self.username if self.username else self.email
    
class Country(models.Model):
    countryName = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.countryName

    
class Guest(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    destination = models.ForeignKey(Destination, null=True, on_delete=models.SET_NULL)
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.SET_NULL)
    airline = models.ForeignKey(Airline, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # First_name = models.ForeignKey(CustomUser, null=True, blank=True,on_delete=models.CASCADE)
    # phoneNo = models.ForeignKey(CustomUser, null=True, blank=True,on_delete=models.CASCADE)
    # emailA = models.ForeignKey(CustomUser, unique=True,on_delete=models.CASCADE) 
    

    # def __str__(self):
    #     return self.arrival_date

