from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from ecom.models import Customer
from reseller.models import Resellers


# Create your views here.
def mngreseller(request):
    return render(request, "admin/manage_resellers.html")


def addreseller(request):
    reqdata = Resellers.objects.filter(status='inactive')
    print(reqdata)
    return render(request, "admin/add_reseller.html", {"userrequests": reqdata})


def deletereseller(request):
    return render(request, "admin/delete_resellers.html")


def admlogin(request):
    if request.method == "POST":
        usrname = request.POST['admuser']
        passwd = request.POST['admpasswd']
        user = authenticate(username=usrname, password=passwd)
        if user is not None:
            try:
                customerdata = Customer.objects.get(login_id=user.id)
                return render(request, "admin/admin_login.html", {"loginerror": "Administartor credentials invalid"})
            except Customer.DoesNotExist:
                try:
                    resellerdata = Resellers.objects.get(login_id=user.id)
                    return render(request, "admin/admin_login.html", {"loginerror": "Administartor credentials invalid"})
                except Resellers.DoesNotExist:
                    return redirect('managereseller')
        else:
            return render(request, "admin/admin_login.html", {"loginerror": "Administartor credentials invalid"})
    else:
        return render(request, "admin/admin_login.html")
