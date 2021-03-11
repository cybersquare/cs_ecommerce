from django.db import models


# Create your models here.
class UserType (models.Model):
    type = models.CharField(max_length=40)



