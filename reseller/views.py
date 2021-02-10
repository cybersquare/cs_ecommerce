from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, tzinfo
from common.models import Products
from .models import ProductResellerMapping


# Create your views here.
def index(request):
    return HttpResponse("hello cybersquare, welcome")


def reseller_master(request):
    return render(request, "reseller/reseller_master.html")


def reseller_home(request):
    return render(request, "reseller/reseller_home.html")


def reseller_products(request):
    return render(request, "reseller/reseller_products.html")

@csrf_exempt
def reseller_addProducts(request):
    if request.method == 'POST':
        print(request.body) 
        title = request.POST['title']
        regproductid = request.POST['regproductid']
        description = request.POST['description']
        img = request.POST['image']
        price = request.POST['price']
        quantity = request.POST['quantity']
        weight = request.POST['weight']
        weightunit = request.POST['weightunit']
        category = request.POST['category']
        subcategory = request.POST['subcategory']
        vendor = request.POST['vendor']

        user = request.session['resellerid']
        print(vendor)
        product = Products(title = title, regproductid = regproductid, desc = description, img= img, price = price, quantity=quantity,weight=weight,weightunit=weightunit, category=category,subcategory=subcategory, vendor=vendor)
        product.save()

        # mapping = ProductResellerMapping(productid = product.id, resellerid = user.id)
        # print("@@@@@@@",mapping)
    else:
        return render(request, "reseller/reseller_addProduct.html")



def reseller_editProducts(request):
    return render(request, "reseller/edit_product.html")


def return_date_time():
    now = timezone.now()
    return now + timedelta(days=1)
