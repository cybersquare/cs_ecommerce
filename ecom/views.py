from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
# from django.contrib.auth.models import User

from django.contrib.auth import authenticate


# Create your views here.

def home(request):
    return render(request,"ecom/cust_home.html")

def login(request):
    if request.method == 'POST':
        usrname=request.POST['userName']
        passwd=request.POST['userPassword']

        user = authenticate(username=usrname, password=passwd)
        print(user)
   

        if user is not None:
            return redirect('home')
        else:
            return render(request,'ecom/login.html',{'error':'Incorrect user details'})
            
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
    return render(request,"ecom/signup.html")



