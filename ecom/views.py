from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request,"ecom/cust_home.html")

def login(request):
    return render(request,"ecom/login.html")

def signup(request):
    return render(request,"ecom/signup.html")
<<<<<<< HEAD
def search_products(request):
    return render(request,"ecom/search_products.html")
def view_product(request):
    return render(request,"ecom/view_product.html")
=======

>>>>>>> 187b1d382ce95056600fd4a815927747f9e41117
