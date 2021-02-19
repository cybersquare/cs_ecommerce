from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ecom.models import Customer
from reseller.models import Resellers


# Create your views here.
def mngreseller(request):
    return render(request, "admin/manage_resellers.html")


def addreseller(request):
        reqdata = Resellers.objects.filter(status='inactive')
        userdata = User.objects.all()
        return render(request, "admin/add_reseller.html", {"userrequests": reqdata, "alldata": userdata})


def verify_reseller(request):
    userid=request.GET['userid']
    status=request.GET['status']
    # Resellers.objects.filter(login_id_id = userid).update(status=status)
    reseldata=Resellers.objects.all()
    usrdata=User.objects.all()
    resellerdata=[{'companyname': resel.companyname, 'companyid': resel.companyregid, 'address': resel.address, 'country': resel.country, 'mobile': resel.mobile, 'bankaccountholder': resel.bankaccountholder, 'bankacccountnumber': resel.bankacccountnumber, 'bankacccountifsc': resel.bankacccountifsc, 'login_id_id': resel.login_id_id, 'status': resel.status} for resel in reseldata]
    userdata=[{'email': usr.email, 'joindate': usr.date_joined} for usr in usrdata]
    return JsonResponse({'usrdata': userdata, 'resellerdata':resellerdata})


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
