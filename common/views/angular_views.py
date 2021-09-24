from itertools import chain
from django.http import response
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from random import randint
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
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
                responseStatus = {"status": "Registration successfull", "otp": customer.otp, "id": user.id}
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
                responseStatus = {"status": "Registration successfull", "otp": reseller.otp, "id": user.id}
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
@api_view(['POST'])
@csrf_exempt
def ang_Login(request):
    if request.method == 'POST':
        logindata = request.data
        username = logindata['userName']
        passwd = logindata['userPassword']
        
        user = authenticate(username=username, password=passwd)
        if user is not None:
            login(request, user)
            try:
                # Login operation for customers
                customerdata = Customer.objects.get(login_id_id=user.id)
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
                    Customer.objects.filter(login_id_id=user.id).update(otp=otp)
                    loginDetails=Customer.objects.get(login_id_id=user.id)
                    # user_login=serializers.serialize('json', [loginDetails])
                    resp={"status": "OTP not verified", "id": user.id,"customerType": "customer", "otp": loginDetails.otp }
                    return Response(resp, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                # if customer already completed otp verification redirect
                # to home page
                else:
                    print("OTP already verified")
                    loginDetails=Customer.objects.get(login_id_id=user.id)
                    resp = {"status": "Login successful", "customerType": "customer" , "id": user.id}
                    # customer_login=serializers.serialize('json', [loginDetails])
                    return Response(resp, status=status.HTTP_200_OK)

            except Customer.DoesNotExist:
                print("Exception working")
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
                    loginDetails=Resellers.objects.get(login_id=user.id)
                    # user_login=serializers.serialize('json', [customerdata])
                    resp={"status": "OTP not verified", "id": user.id,"customerType": "reseller", "otp": loginDetails.otp }
                    return Response(resp, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                # if Reseller already completed otp verification
                # redirect to home page
                else:
                    print("OTP already verified")
                    loginDetails=Resellers.objects.get(login_id=user.id)
                    # user_login=serializers.serialize('json', [customerdata])
                    resp = {"status": "Login successful","customerType": "reseller", "id": user.id}
                    return Response(resp, status=status.HTTP_200_OK)
        # If credentials are wrong, paasing a error message
        else:
            responseStatus = {"status": "Login Failed","message": "Please check your username and password"}
            return Response(responseStatus, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# def fnConverQtoList(querySet):
#     return []

# Reseller views section
# Get seller products
@api_view(['POST'])
@csrf_exempt
def get_res_products(request):
    if request.method == "POST":
        userdata=request.data
        # loginid = int('2')
        loginid = int(userdata['id'])
        resllerdetails=Resellers.objects.get(login_id=loginid)
        products = Products.objects.filter(reseller_id=resllerdetails.id)
        if not products:
            return Response('no products', status=status.HTTP_200_OK)
        else:
            print(products)
            # products = fnConverQtoList(products)
            prod_list=[]
            for prod in products:
                prod_list.append({"productId": prod.id ,"title": prod.title, "reg_productid": prod.reg_productid, "desc": prod.desc, "vendor": prod.vendor,"price": prod.price,"quantity":prod.quantity,"weight": prod.weight,"weightunit": prod.weightunit,"category": prod.category,"subcategory": prod.subcategory ,"status": prod.status, "imgURl": prod.img.url})
            # products.append({"stat","prod available"})
            # productdetails = serializers.serialize('json', products)
        return Response(prod_list, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def approveReseller(request):
    if request.method == "GET":
        resdata=Resellers.objects.filter(status="inactive").select_related('login')
        login_data=[]
        for res in resdata:
            resp = {"rId": res.login.id, "rName": res.companyname, "rAddress": res.address, "email": res.login.username, "contact": res.mobile, "AccNumber": res.bankacccountnumber, "AccIFSC":res.bankacccountifsc, "AccHolderName":res.bankaccountholder}
            login_data.append(resp)
        return Response(login_data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@csrf_exempt
def AngProfileView(request):
    if request.method == "POST":
        userdata= json.loads(request.body)
        id = int(userdata['id'])
        usertype = userdata['usertype']
        if usertype == "customer":
            userdata = Customer.objects.select_related('login_id').get(login_id_id=id)
            response={"name": userdata.firstname, "address": userdata.address, "dob": userdata.dateofbirth, "gender": userdata.gender, "country": userdata.country, "mobile": userdata.mobile, "email":userdata.login_id.username}
        elif usertype == "reseller":
            userdata = Resellers.objects.select_related('login').get(login_id=id)
            response={"Rname": userdata.companyname,"Rid": userdata.companyregid,"address":userdata.address,"usertype":"reseller", "country": userdata.country, "mobile": userdata.mobile, "email":userdata.login.email}
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@csrf_exempt
def AngVerifyReseller(request):
    if request.method == "PUT":
        resellerdata=json.loads(request.body)
        userid=int(resellerdata['id'])
        ResStatus=resellerdata['status']
        Resellers.objects.filter(login_id=userid).update(status=ResStatus)
        resp = {'status': "success", 'msg':"Reseller request updated"}
        return Response(resp,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@csrf_exempt
def AngViewReseller(request):
    if request.method == "GET":
        resellerdata=Resellers.objects.all().select_related('login')
        resellerList=[]
        for reseller in resellerdata:
            resp={"rName":reseller.companyname, "rAddress":reseller.address, "email": reseller.login.email, "contact": reseller.mobile }
            resellerList.append(resp)
        # resellerdata = serializers.serialize('json', resellerdata)
        return Response(resellerList, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def AngAdminLogin(request):
    if request.method == "POST":
        admindata = request.data
        usrname = admindata['user']
        passwd = admindata['password']
        user = authenticate(username=usrname, password=passwd)
        if user is not None:
            if Customer.objects.filter(login_id=user.id) or Resellers.objects.filter(login_id=user.id):
                resp={"status": "failed"}
                return Response( resp, status=status.HTTP_200_OK)
            else:
                resp={"status": "success", "adminid": user.id}
                return Response( resp, status=status.HTTP_200_OK)
        else:
            resp={"status": "failed"}
            return Response( resp, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def ResAddProduct(request):
    try:
        print("Execution started")
        data=request.data
        title = data['title']
        regproductid = data['regproductid']
        description = data['description']
        img = request.FILES['imageURL']
        price = data['price']
        quantity = data['quantity']
        weight = data['weight']
        weightunit = data['weightunit']
        # imgUrl=data['imageURL']
        category = data['category']
        subcategory = data['subcategory']
        vendor = data['vendor']
        status = data['status']
        resellerid = data['resellerid']
        resllerdetails=Resellers.objects.get(login_id=resellerid)
        product = Products(title=title, reg_productid=regproductid, desc=description, img=img, price=price, quantity=quantity, weight=weight, weightunit=weightunit, category=category, subcategory=subcategory, vendor=vendor, status=status, reseller_id=resllerdetails.id)
        product.save()
        product_id = product.pk
        return Response({'status': "Success"})   
    except KeyError:
        return Response({'staus': 'failed'})


@api_view(['POST'])
@csrf_exempt
def search_products(request):
    # search data based on keyword
    if request.method == "POST":
        data=request.data
        search_word = data['searchdata']
        search_list=search_word.split(' ')
        srch_products=Products.objects.filter(Q(title__icontains=search_word) | Q(vendor__icontains=search_word) | Q(category__icontains=search_word) | Q(subcategory__icontains=search_word), status='Active')
        # Rendering search product page
        # print(srch_products)
        resp=[]
        for res in srch_products:
            resp.append({"id":res.id,"title":res.title,"reg_productid":res.reg_productid,"desc":res.desc,"price":res.price,"vendor":res.vendor})
        if len(resp) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(resp, status=status.HTTP_200_OK)   


@api_view(['POST'])
@csrf_exempt
def resDeleteProducts(request):
    if request.method == "POST":
        data=request.data
        get_id= int(data['product_id'])
        try:
            instance = Products.objects.get(id=get_id)
            instance.delete()
            return Response({'msg':'The product deleted'}, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@csrf_exempt
def resUpdateProducts(request):
    if request.method == "POST":
        data=request.data
        get_id= int(data['product_id'])
        try:
            Products.objects.filter(id=get_id).update(title=data['title'], desc=data['description'], price=data['price'], quantity=data['quantity'], status=data['status'])
            return Response({'msg':'The product updated successfully'}, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@csrf_exempt
def changepassword(request):
    if request.method == "POST":
        data=request.data
        username = data['usrname']
        password = data['newpassword']
        old_pass = data['oldpassword']
        try:
            user = User.objects.get(username=username)

            # Verifying customer otp and changing password
            usr = authenticate(username=username, password=old_pass)
            if usr is not None:
                user.set_password(password)
                user.save()
                return Response({"message": 'Your password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"message": 'incorrect password'},)
        except User.DoesNotExist:
            return Response({"message": 'invalid username'},status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@csrf_exempt
def Ang_view_product(request):
    data=request.data
    id=int(data['productid'])
    productdetails = Products.objects.get(id=id)
    respDetails={"prodid": productdetails.id ,"title": productdetails.title, "regProductid": productdetails.reg_productid, "description": productdetails.desc, "price": productdetails.price, "weight": productdetails.weight, "weightunit": productdetails.weightunit, "category": productdetails.category, "subcategory": productdetails.subcategory, "vendor": productdetails.vendor}
    return Response(respDetails, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def Ang_addToCart(request):
    try:
        data=request.data
        prod_id=int(data['prodid'])
        quantity=int(data['quantity'])
        cust_id=int(data['customerid'])
        orderdata=Orders(product_id_id=prod_id,quantity=quantity,customerid_id=cust_id,status='added_to_bag')
        orderdata.save()
        return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({"message": "Something went wrong"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


@api_view(['POST'])
@csrf_exempt
def AngViewCart(request):
    if request.method == "POST":
        try:
            data=request.data
            cust_id = int(data['customerid'])
            bagdata = Orders.objects.filter(customerid=cust_id, status='added_to_bag').select_related('product_id')
            # print(bagdata)
            totalAmmount=0
            cartproduct=[]
            cnt=False
            for orderdata in bagdata:
                cnt=True
                totalAmmount=totalAmmount+(orderdata.product_id.price*orderdata.quantity)
                cartproduct.append({"productname": orderdata.product_id.title, "imgurl": orderdata.product_id.img.url, "productPrice": orderdata.product_id.price, "quantity": orderdata.quantity, "productid": orderdata.product_id.id})
            cartdata={"totalAmmount": totalAmmount, "productdata": cartproduct}
            print(cnt)
            if cnt == True:
                return Response(cartdata, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@csrf_exempt
def createOrder(request):
    data=request.data
    userid=int(data['customerid'])
    # products_orderdata = Orders.objects.filter(customerid=userid, status='added_to_bag')
    order_amount = int(data['totalprice'])* 100
    order_currency = 'INR'
    address=data['address']
    order_receipt = 'order_rcptid_11'
    # notes = {'Shipping address': 'Bommanahalli, Bangalore'}
    notes = {'Shipping address': address}
    client = razorpay.Client(auth=('rzp_test_jznmHCFBf6ZMUd','hMGwzenl3b1QwDmJxDtyAUNy'))
    payment = client.order.create({"amount": order_amount, "currency": order_currency, "receipt": order_receipt, 'notes': notes})
    print(payment)
    return Response( payment, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def PlaceOrder(request):
    userid=request.data['customerid']
    Orders.objects.filter(customerid=userid, status='added_to_bag').update(status='paid')
    return Response({'resp': "success"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def viewOrders(request):
    try:
        cust_id = request.data['customerid']
        bagdata = Orders.objects.filter(customerid_id=cust_id).exclude(status__in='added_to_bag').select_related('product_id')
        # bag_ids = bagdata.values_list('product_id_id')
        # productdata = Products.objects.filter(id__in=bag_ids)
        price = 0
        purchasedetails=[]
        totAmmount=0
        for bgdata in bagdata:
            # resp={"orderdate": bgdata.orderdate}
            price=bgdata.product_id.price * bgdata.quantity
            totAmmount= totAmmount+price
            purchasedetails.append({"orderdate": bgdata.orderdate, "productName": bgdata.product_id.title, "ammount": price, "quantity": bgdata.quantity})
        resp={"totalammount": totAmmount, "purchaseproducts": purchasedetails}
        # for prod in productdata:
        #     for bg in bagdata:
        #         if bg.product_id_id == prod.id:
        #             price = price + (bg.quantity * prod.price)
        # print(price)
        return Response(resp)
    except Orders.DoesNotExist:
        return Response({"customerid": "1"})


@api_view(['POST'])
@csrf_exempt
def AngEditProfile(request):
    data= request.data
    address = data['address']
    country = data['country']
    mobile = data['mobile']
    fname = data['firstname']
    id = int(data['customerid'])
    if data['customertype'] == "customer": 
        lname = data['lastname']
        User.objects.filter(id=id).update(first_name=fname, last_name=lname)
        Customer.objects.filter(login_id_id=id).update(firstname=fname, mobile=mobile, address=address, country=country,)
    # custdata = Customer.objects.get(login_id_id=id)
    # customerdata = {'firstname': custdata.firstname, 'gender': custdata.gender, 'dateofbirth': custdata.dateofbirth, 'mobile': custdata.mobile, 'address': custdata.address, 'country': custdata.country}
    # userdata = User.objects.get(id=id)
    # usrdata = {'lastname': userdata.last_name, 'email': userdata.email }
    else:
        User.objects.filter(id=id).update(first_name=fname)
        Resellers.objects.filter(login_id=id).update(companyname=fname, mobile=mobile, address=address, country=country)
    return Response({"msg": "Profile updated"}, status=status.HTTP_200_OK)