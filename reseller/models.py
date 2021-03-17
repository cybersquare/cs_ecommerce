from django.db import models
from django.contrib.auth.models import User
from common.models import UserType
# from .views import return_date_time
from datetime import datetime



# Create your models here.
class Resellers(models.Model):
    companyname = models.CharField(max_length=30)
    companyregid = models.CharField(max_length=12)
    address = models.CharField(max_length=70)
    country = models.CharField(max_length=30)
    mobile = models.CharField(max_length=12)
    bankaccountholder = models.CharField(max_length=30)
    bankacccountnumber = models.CharField(max_length=30)
    bankacccountifsc = models.CharField(max_length=30)
    # usertype as the foriegn key of user type table
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default= 'inactive')
    requestdate = models.DateField(default=datetime.now)
    otp = models.CharField(max_length=70)
    # requestdate = models.DateField(default=return_date_time)
    def __str__(self): 
         return self.companyname

class Products(models.Model):
    title = models.CharField(max_length=30)
    reg_productid = models.CharField(max_length=12)
    desc = models.TextField()
    img = models.ImageField(upload_to = 'product_images/', blank = True, null = True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    weight = models.IntegerField()
    weightunit = models.CharField(max_length=12)
    category = models.CharField(max_length=12)
    subcategory = models.CharField(max_length=12)
    vendor = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    reseller = models.ForeignKey(Resellers, on_delete=models.CASCADE)
    def __str__(self): 
         return self.title







