from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from reseller.models import Resellers
# from django.contrib.auth.models import User

from django.contrib.auth import authenticate


# Create your views here.

def home(request):
    # newuser = User.objects.create_user('administrator', 'ecomadmin@cs.com', 'Admin@123')
    # newuser.save()
    return render(request,"ecom/cust_home.html")
    
def login(request):
    if request.method == 'POST':
        usrname = request.POST['userName']
        passwd = request.POST['userPassword']
        user = authenticate(username=usrname, password=passwd)
        if user is not None:
            try:
                customerdata = Customer.objects.get(login_id = user.id)
                request.session['customerid']=user.id
                return redirect('home')
                

            except Customer.DoesNotExist:
                return redirect('/reseller/home')

        else:
            return render(request,'ecom/login.html',{'error':'Invalid user details'})
            
        # try:
        #     logindata = User.objects.get(username=usrname)
        #     # logindata = User.objects.get(username=usrname)
        #     if  logindata.password == passwd:
        #         return redirect('home')
        #     else:
        #         return HttpResponse("Incorrect password")
        # except User.DoesNotExist:
        #     return HttpResponse("Invalid username")
        # return HttpResponse(passwd)

    else:
        return render(request,"ecom/login.html")


def signup(request):
    if request.method == "POST":
        usertype = request.POST['usertype']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST['gender']
        dateofbirth = request.POST['dateofbirth']
        address = request.POST['address']
        country = request.POST['country']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']

        #reseller specific information   
        resellercompanyname = request.POST['resellercompanyname']
        resellercompanyid = request.POST['resellercompanyid']
        resellerbankaccountname = request.POST['resellerbankaccountname']
        resellerbankaccountnumber = request.POST['resellerbankaccountnumber']
        resellerbankaccountifsc = request.POST['resellerbankaccountifsc']


       
        if usertype == 'customer':
            newuser = User.objects.create_user(email, email, password)
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.save()
            customerdata = Customer(firstname=firstname,gender=gender,mobile=mobile,dateofbirth=dateofbirth,address=address,country=country,user_type_id=1,login_id_id=newuser.id)
            customerdata.save()
            return redirect('login')
        else:
            newuser = User.objects.create_user(email, email, password)
            newuser.save()
            resellerdata = Resellers(companyname=resellercompanyname,companyregid=resellercompanyid,address=address,country=country,mobile=mobile,bankaccountholder=resellerbankaccountname,bankacccountnumber = resellerbankaccountnumber,bankacccountifsc=resellerbankaccountifsc,user_type_id=2,login_id_id=newuser.id)
            resellerdata.save()
            return redirect('login')
    else:
        return render(request,"ecom/signup.html")

def search_products(request):
    return render(request,"ecom/search_products.html")
def view_product(request):
    return render(request,"ecom/view_product.html")

