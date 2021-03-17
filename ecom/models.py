from django.db import models
from django.contrib.auth.models import User
from common.models import UserType
from reseller.models import Products
import datetime


# Create your models here.
class Customer(models.Model):
    firstname = models.CharField(max_length=30)
    mobile = models.CharField(max_length=12)
    gender = models.CharField(max_length=6)
    dateofbirth = models.DateField()
    address = models.CharField(max_length=70)
    country = models.CharField(max_length=30)
    status = models.CharField(max_length=20, default="")
    # usertype as the foriegn key of user type table
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    login_id = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=70)
    def __str__(self): 
         return self.firstname


class Orders(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    customerid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orderdate = models.DateField(default=datetime.date.today)
    quantity = models.IntegerField()
    status = models.CharField(max_length=30)
    def __str__(self): 
         return self.product_id


class Payment(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    ammount = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)