from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_type (models.Model):
    type=models.CharField(max_length=40)