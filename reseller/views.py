from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, tzinfo
from common.models import Products
from .models import ProductResellerMapping, Resellers


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
        
        resellerid = Resellers.objects.get(login_id_id=user)
        product = Products(title = title, regproductid = regproductid, desc = description, img= img, price = price, quantity=quantity,weight=weight,weightunit=weightunit, category=category,subcategory=subcategory, vendor=vendor)
        product.save()
        
        mapping = ProductResellerMapping(productid_id = product.id, resellerid_id = resellerid.id)
        mapping.save()
        
    else:
        return render(request, "reseller/reseller_addProduct.html")


@csrf_exempt
def reseller_editProducts(request):
    if request.method == "POST":
        id=request.POST['id']
        title=request.POST['product_title']
        print(title)
        description=request.POST['product_description']
        print(description)
        image=request.POST['product_image']
        print(image)
        price=request.POST['product_price']
        print(price)
        quantity=request.POST['product_quantity']
        print(quantity)
        weight=request.POST['product_weight']
        print(weight)
        unit=request.POST['weight_unit']
        print(unit)
        return JsonResponse({'message': "data inserted successfully"})
    else:
        return render(request, "reseller/edit_product.html")


def return_date_time():
    now = timezone.now()
    return now + timedelta(days=1)
