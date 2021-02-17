from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, tzinfo
from common.models import Products
from .models import ProductResellerMapping, Resellers
from random import randint
from django.core.files.storage import FileSystemStorage


# Create your views here.
def index(request):
    return HttpResponse("hello cybersquare, welcome")


def reseller_master(request):
    return render(request, "reseller/reseller_master.html")


def reseller_home(request):
    # print(request.session['resellerid'])
    return render(request, "reseller/reseller_home.html")


def reseller_products(request):
    return render(request, "reseller/reseller_products.html")


@csrf_exempt
def reseller_addProducts(request):
    if request.method == 'POST':
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
        print(request.session['resellerid'])
        user = request.session['resellerid']
        resellerid = Resellers.objects.get(login_id_id=user)
        product = Products(title=title, regproductid=regproductid, desc=description, img=img, price=price, quantity=quantity, weight=weight, weightunit=weightunit, category=category, subcategory=subcategory, vendor=vendor)
        product.save()
        mapping = ProductResellerMapping(productid_id=product.id, resellerid_id=resellerid.id)
        mapping.save()
    else:
        print(request.session['resellerid'])
        return render(request, "reseller/reseller_addProduct.html")


@csrf_exempt
def reseller_editProducts(request):
    # Check request ajax or not
    if request.is_ajax:
        if request.method == "POST":
            prdid = request.POST['id']
            product_description = request.POST['description']
            # Store image to a variable
            image = request.FILES['image']
            price = request.POST['price']
            quantity = request.POST['quantity']
            # Upload file to media directory
            # fs = FileSystemStorage()
            # filename = fs.save(image.name, image)
            # uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url)
            # print(image.name)
            Products.objects.filter(id=prdid).update(desc=product_description, price=price, img=image, quantity=quantity)
            # print("Success")
            return JsonResponse({'message': "data inserted successfully"})
        else:
            # return edit page with selected product data
            product = Products.objects.get(id=1)
            print(product)
            return render(request, "reseller/edit_product.html", {'product': product})


def return_date_time():
    now = timezone.now()
    return now + timedelta(days=1)
