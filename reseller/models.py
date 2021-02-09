from django.db import models
from django.contrib.auth.models import User
from common.models import UserType
from .views import return_date_time


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
    login_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default= 'inactive')
    requestdate = models.DateField(default=return_date_time)
