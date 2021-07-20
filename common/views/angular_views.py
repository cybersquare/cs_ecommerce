from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from random import randint
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate, login, logout
import json

# importing models from app
from ecom.models import Customer, User, Orders, Payment
from reseller.models import Resellers,Products
# Create your views here.

# return all products details
def ang_view_product(request):
    all_products=Products.objects.all()
    allproductlist = serializers.serialize('json', all_products)
    print(allproductlist)
    return HttpResponse(allproductlist, content_type="application/json")

# insert login credentials
@csrf_exempt
@api_view(['GET', 'POST'])
def ang_signup(request):
    # Perform signup operations
    if request.method == "POST":
        # Read common information for customer and reseller from HttpRequest
        userdetails = request.data
        usertype = userdetails['usertype']
        address = userdetails['address']
        country = userdetails['country']
        mobile = userdetails['mobile']
        email = userdetails['email']
        password = userdetails['password']
        # Check user exist or not
        try:
            user= User.objects.get(username=email)
            responseStatus = [{"msg": "User already exist"}]
            return Response(responseStatus, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            # Generate otp and sending to mail
            otp = randint(1000, 9999)
            send_mail(
                    'please verify your otp',
                    str(otp),
                    EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            if usertype == 'customer':
                # Read customer specific information and signing up
                firstname = userdetails['firstname']
                lastname = userdetails['lastname']
                gender = userdetails['gender']
                dateofbirth = userdetails['dateofbirth']
                newuser = User.objects.create_user(email, email, password)
                newuser.first_name = firstname
                newuser.last_name = lastname
                newuser.save()
                customerdata = Customer(firstname=firstname,gender=gender, mobile=mobile, dateofbirth=dateofbirth, address=address, country=country, user_type_id=1, login_id_id=newuser.id, status='otpverify', otp=str(otp))
                customerdata.save()
                user = User.objects.get(username=email)
                customer = Customer.objects.get(login_id_id=user.id)
                newuserdetails = serializers.serialize('json', [customer])
                responseStatus = [{"msg": "Registreration successfull"}]
                return Response(responseStatus, newuserdetails, status=status.HTTP_201_CREATED)
            else:
                # Read reseller specific information and signing up
                resellercompanyname = userdetails['resellercompanyname']
                resellercompanyid = userdetails['resellercompanyid']
                resellerbankaccountname = userdetails['resellerbankaccountname']
                resellerbankaccountnumber = userdetails['resellerbankaccountnumber']
                resellerbankaccountifsc = userdetails['resellerbankaccountifsc']
                newuser = User.objects.create_user(email, email, password)
                newuser.save()
                resellerdata = Resellers(companyname=resellercompanyname, companyregid=resellercompanyid, address=address, country=country, mobile=mobile, bankaccountholder=resellerbankaccountname, bankacccountnumber=resellerbankaccountnumber, bankacccountifsc=resellerbankaccountifsc, user_type_id=2, login_id=newuser.id, status='otpverify', otp=str(otp))
                resellerdata.save()
                user = User.objects.get(username=email)
                reseller = Resellers.objects.get(login_id=user.id)
                newuserdetails = serializers.serialize('json', [reseller])
                # responseStatus = [{"msg": "User registred successfully", "status_code": "201"}]
                responseStatus = [{"msg": "Registreration successfull"}]
                return Response(newuserdetails, responseStatus, status=status.HTTP_201_CREATED)
    # Rendering signup page
    else:
        responseStatus = [{"msg": "An error occured while login"}]
        return Response(newuserdetails, responseStatus, status=status.HTTP_400_BAD_REQUEST)


# OTP verification
def otpVerify(request):
    # Verifying otp if method POST
    if request.method == "POST":
        # id = request.session['otpid']
        # otp = request.POST['inp_otp']
        try:
            userdata = Customer.objects.get(login_id_id=id)
            # Verifying OTP in customer table
            if(otp == userdata.otp):
                Customer.objects.filter(login_id_id=id).update(status='active')
                return redirect('/ecom/home')
            else:
                return render(request, "ecom/verify_otp.html", {"msg": "Invalid otp"})
        except Customer.DoesNotExist:
            userdata = Resellers.objects.get(login_id=id)
            # Verifying OTP in reseller table
            if(otp == userdata.otp):
                Resellers.objects.filter(login_id=id).update(status='inactive')
                return redirect('/reseller/home')
            else:
                return render(request, "ecom/verify_otp.html", {"msg": "Invalid otp"})