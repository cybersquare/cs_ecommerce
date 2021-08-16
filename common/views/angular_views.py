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
@csrf_exempt
@api_view(['GET', 'POST'])
def ang_view_product(request):
    if request.method=="GET":
        all_products=Products.objects.all()
        allproductlist = serializers.serialize('json', all_products)
        return Response(allproductlist, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

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
            responseStatus = {"status": "User already exist"}
            return Response(responseStatus, status=status.HTTP_208_ALREADY_REPORTED)
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
                # newuserdetails = serializers.serialize('json', [customer])
                responseStatus = {"status": "Registeration successfull", "otp": customer.otp, "id": user.id}
                return Response( responseStatus, status=status.HTTP_201_CREATED)
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
                # newuserdetails = serializers.serialize('json', [reseller])
                responseStatus = {"status": "Registeration successfull", "otp": reseller.otp, "id": user.id}
                return Response(responseStatus, status=status.HTTP_201_CREATED)
    # Rendering signup page
    else:
        responseStatus = {"status": "Invalid request type"}
        return Response(responseStatus)


# OTP verification
@csrf_exempt
@api_view(['GET', 'POST'])
def otpVerification(request):
    # Verifying otp if method POST
    if request.method == "POST":
        # Read common information for customer and reseller from HttpRequest
        userdetails = request.data
        id = int(userdetails['userid'])
        # Updating OTP status
        if Customer.objects.filter(login_id_id=id).exists():
            # userdata = Customer.objects.get(login_id_id=id)
            # Customer otp verification
            Customer.objects.filter(login_id_id=id).update(status='active')
            responseStatus = {"status": "OTP verified successfully"}
            return Response(responseStatus, status=status.HTTP_200_OK)
        elif Resellers.objects.filter(login_id=id).exists():
            # Reseller OTP verification
            Resellers.objects.filter(login_id=id).update(status='inactive')
            responseStatus = {"status": "OTP verified successfully"}
            return Response(responseStatus, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Login process
@api_view(['GET', 'POST'])
@csrf_exempt
def ang_Login(request):
    if request.method == 'POST':
        logindata = request.data
        username = logindata['userName']
        passwd = logindata['userPassword']
        print("Authentication startsssssss")
        user = authenticate(username=username, password=passwd)
        if user is not None:
            login(request, user)
            try:
                # Login operation for customers
                customerdata = Customer.objects.get(login_id=user.id)
                # if customer didn't complete otp verification send otp and verifying it
                if customerdata.status == 'otpverify':
                    print("OTP verification working")
                    otp = randint(1000, 9999)
                    send_mail(
                        'please verify your otp',
                        str(otp),
                        EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    Customer.objects.filter(login_id=user.id).update(otp=otp)
                    loginDetails=Customer.objects.filter(login_id=user.id)
                    # user_login=serializers.serialize('json', [loginDetails])
                    resp={"msg": "otp verify", "id": user.id,"customerType": "customer", "otp": loginDetails.otp }
                    return Response(resp, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                # if customer already completed otp verification redirect
                # to home page
                else:
                    print("OTP already verified")
                    loginDetails=Customer.objects.filter(login_id=user.id).values('login_id')
                    resp = {"msg": "Login successfull", "customerType": "customer" , "id": user.id}
                    # customer_login=serializers.serialize('json', [loginDetails])
                    return Response(resp, status=status.HTTP_200_OK)

            except Customer.DoesNotExist:
                # Login operation for resellers
                resellerdata = Resellers.objects.get(login_id=user.id)
                # if Reseller didn't complete otp verification send otp and verifying it
                if resellerdata.status == 'otpverify':
                    print("OTP verification working")
                    # Generate otp and sending to mail
                    otp = randint(1000, 9999)
                    send_mail(
                        'please verify your otp',
                        str(otp),
                        EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    Resellers.objects.filter(login_id=user.id).update(otp=otp)
                    # loginDetails=Customer.objects.filter(login_id=user.id).first()values('login_id','otp')
                    loginDetails=Customer.objects.filter(login_id=user.id)
                    # user_login=serializers.serialize('json', [customerdata])
                    resp={"msg": "otp verify", "id": user.id,"customerType": "reseller", "otp": loginDetails.otp }
                    return Response(resp, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                # if Reseller already completed otp verification
                # redirect to home page
                else:
                    print("OTP already verified")
                    loginDetails=Customer.objects.filter(login_id=user.id)
                    # user_login=serializers.serialize('json', [customerdata])
                    resp = {"msg": "Login successfull","customerType": "reseller", "id": user.id}
                    return Response(resp, status=status.HTTP_200_OK)
        # If credentials are wrong, paasing a error message
        else:
            responseStatus = {"status": "Login Failed.... Please check your username and password are correct"}
            return Response(responseStatus, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Reseller views section
# Get seller products
@csrf_exempt
@api_view(['GET', 'POST'])
def get_res_products(request):
    if request.method == "POST":
        userdata=json.loads(request.body)
        print(userdata[id])
        # loginid = int('2')
        loginid = int(userdata.id)
        products = Products.objects.filter(reseller_id=loginid)
        productdetails = serializers.serialize('json', products)
        return Response(productdetails, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)