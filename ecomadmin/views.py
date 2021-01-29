from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def mngreseller(request):
    return render(request,"admin/manage_resellers.html")

def addreseller(request):
    return render(request,"admin/add_reseller.html")

def deletereseller(request):
    return render(request,"admin/delete_resellers.html")

def admlogin(request):
    return render(request,"admin/admin_login.html")