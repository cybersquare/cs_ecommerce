from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("hello cybersquare, welcome")
def reseller_home(request):
    return render(request,"Reseller_home.html")
def reseller_products(request):
    return render(request,"Reseller_products.html")




