from django.db import models


# Create your models here.
class UserType (models.Model):
    type = models.CharField(max_length=40)


class TrainingModel(models.Model):
    firstname = models.CharField(max_length=12)
    lastname = models.CharField(max_length=12)
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=6)
