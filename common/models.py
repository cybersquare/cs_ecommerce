from django.db import models



# Create your models here.
class UserType (models.Model):
    type = models.CharField(max_length=40)


class Products(models.Model):
    title = models.CharField(max_length=30)
    regproductid = models.CharField(max_length=12)
    desc = models.TextField()
    img = models.ImageField(upload_to = 'pics')
    price = models.IntegerField()
    quantity = models.IntegerField()
    weight = models.IntegerField()
    weightunit = models.CharField(max_length=12)
    category = models.CharField(max_length=12)
    subcategory = models.CharField(max_length=12)
    vendor = models.CharField(max_length=30)

