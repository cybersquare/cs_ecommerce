from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from ecom.models import Customer

# Create your views here.
def mngreseller(request):
    return render(request,"admin/manage_resellers.html")

def addreseller(request):
    return render(request,"admin/add_reseller.html")

def deletereseller(request):
    return render(request,"admin/delete_resellers.html")

def admlogin(request):
    if request.method == "POST":
        usrname = request.POST['admuser']
        passwd = request.POST['admpasswd']
        user = authenticate(username=usrname, password=passwd)
        if user is not None:
            try:
                customerdata = Customer.objects.get(login_id = user.id)
                return render(request,"admin/admin_login.html",{"loginerror" : "Administartor credentials invalid"})
            except Customer.DoesNotExist:
                try:
                    resellerdata = Reseller.objects.get(login_id = user.id)
                    return render(request,"admin/admin_login.html",{"loginerror" : "Administartor credentials invalid"})
                except Reseller.DoesNotExist:
                    return redirect('managereseller')
           
        else:
            return render(request,"admin/admin_login.html",{"loginerror" : "Administartor credentials invalid"})
    else:
        return render(request,"admin/admin_login.html")

