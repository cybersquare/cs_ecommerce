from django.db import models
from django.contrib.auth.models import User
from common.models import UserType


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
