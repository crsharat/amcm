from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db import models
# Create your models here.


class Resident(AbstractBaseUser):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_staff = False
    mobile_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    city = models.ForeignKey('resident.City', on_delete=models.PROTECT)
    state = models.ForeignKey('resident.State', on_delete=models.PROTECT)
    country = models.ForeignKey('resident.Country', on_delete=models.PROTECT)
    dob = models.DateField(max_length=8)
    active = models.BooleanField(default=True)
    owner = models.BooleanField(default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email']

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_location(self):
        return f"{self.city.name}, {self.state.name}, {self.country.name}"
    

class City(models.Model):
    state = models.ForeignKey('resident.State', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey('resident.Country', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Flat(models.Model):
    number = models.CharField(max_length=15)
    bhk = models.IntegerField(default=3)
    square_feet = models.IntegerField()
    elecno = models.CharField(max_length=50)
    wardno = models.CharField(max_length=50)


class FlatRecords(models.Model):
    resident = models.ForeignKey('resident.Resident', null=True, on_delete=models.SET_NULL)
    adults = models.IntegerField()
    children = models.IntegerField(default=0)
    flat_acquired = models.DateTimeField(default=timezone.now)
    moved_out = models.DateTimeField(null=True, blank=True)

# class Payment(models.Model):
#   flat = models.ForeignKey('resident.Flat')
#   amount = models.DecimalField(deicmal_places=3)
#   payed_on = models.DateTimeField(timezone.now())
#   payment_method = 
