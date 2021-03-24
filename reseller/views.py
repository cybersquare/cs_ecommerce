from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, tzinfo
from .models import Resellers, Products
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
    loginid = request.session['resellerid']
    resellerid = Resellers.objects.get(login_id=loginid)
    products = list(Products.objects.all().values().filter(reseller_id=resellerid))
    return render(request, "reseller/reseller_products.html", {'products': products})


@csrf_exempt
def reseller_addProducts(request):
    if request.method == 'POST':
        title = request.POST['title']
        regproductid = request.POST['regproductid']
        description = request.POST['description']
        img = request.FILES['image']
        price = request.POST['price']
        quantity = request.POST['quantity']
        weight = request.POST['weight']
        weightunit = request.POST['weightunit']
        category = request.POST['category']
        subcategory = request.POST['subcategory']
        vendor = request.POST['vendor']
        status = request.POST['status']
        user = request.session['resellerid']
        resellerid = Resellers.objects.filter(login_id=user).values_list('id', flat=True).get()
        product = Products(title=title, reg_productid=regproductid, desc=description, img=img, price=price, quantity=quantity, weight=weight, weightunit=weightunit, category=category, subcategory=subcategory, vendor=vendor, status=status, reseller_id=resellerid)
        product.save()
        product_id = product.pk
        return JsonResponse({'msg':'successfully added'})    
        if product_id.exists():
            return JsonResponse({'msg':'successfully added'})
        else:
            return JsonResponse({'msg':'Something went wrong'})
    else:
        return render(request, "reseller/reseller_addProduct.html")


def reseller_deleteProducts(request):
    if request.method == "GET":
        get_id= int(request.GET.get('id'))
        instance = Products.objects.get(id=get_id)
        instance.delete()
        return JsonResponse({'msg':'The product deleted'})


@csrf_exempt
def reseller_editProducts(request,id):
    if request.method == "GET":
        product = list(Products.objects.all().values().filter(id=id))
        print(product[0])
        return render(request, "reseller/edit_product.html", {'product': product[0]})

    
@csrf_exempt
def reseller_updateProducts(request):
    if request.method == "POST":
        print("haai hello")
        product_id = request.POST['id']
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        status = request.POST['status']
        print("$$$$", quantity)
        Products.objects.filter(id=product_id).update(title=title, desc=description, price=price, quantity=quantity, status=status)
        

def return_date_time():
    now = timezone.now()
    return now + timedelta(days=1)
