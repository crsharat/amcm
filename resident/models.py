from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin
# Create your models here.


class Resident(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=35, unique=True)
    email = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    city = models.ForeignKey('resident.City', on_delete=models.PROTECT, null=True)
    state = models.ForeignKey('resident.State', on_delete=models.PROTECT, null=True)
    country = models.ForeignKey('resident.Country', on_delete=models.PROTECT, null=True)
    dob = models.DateField(max_length=8, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    owner = models.BooleanField(default=True)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


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
    resident = models.ForeignKey('resident.Resident', null=True, on_delete=models.SET_NULL)

    @property
    def name(self):
        return self.number


class FlatRecords(models.Model):
    resident_flat = models.ForeignKey('resident.Flat', null=True, on_delete=models.SET_NULL)
    adults = models.IntegerField()
    children = models.IntegerField(default=0)
    flat_acquired = models.DateTimeField(default=timezone.now)
    moved_out = models.DateTimeField(null=True, blank=True)


class PaymentMethod(models.Model):
    months = [i+1 for i in range(12)]
    month_choices = tuple(zip(months, months))
    year_choices = tuple(zip([2019, 2020, 2021, 2022], [2019, 2020, 2021, 2022]))
    flat = models.ForeignKey('resident.Flat', null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(decimal_places=3, max_digits=16)
    payed_on = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField(default=1, choices=month_choices)
    year = models.IntegerField(default=2019, choices=year_choices)
    payment_method = models.CharField(max_length=50)
    bank = models.CharField(max_length=20)
    payment_ref = models.CharField(max_length=20)
    receipt_number = models.CharField(max_length=50)
    purpose = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.receipt_number = f"{self.year}-{self.month}-{self.flat}-{self.payment_ref}"
        print(self.receipt_number)
        print(len(self.receipt_number))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_number