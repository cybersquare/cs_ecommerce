from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("hello cybersquare, welcome")
def reseller_master(request):
    return render(request,"reseller/reseller_master.html")
def reseller_home(request):
    return render(request,"reseller/reseller_home.html")
def reseller_products(request):
    return render(request,"reseller/reseller_products.html")
def reseller_addProducts(request):
    return render(request,"reseller/reseller_addProduct.html")





