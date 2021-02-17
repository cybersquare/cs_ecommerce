# flake8:noqa: E501
from django.shortcuts import render, redirect
from ecommerce.decoratos import cust_login_required
from .models import Customer, User
from reseller.models import Resellers
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
# from django.conf import settings
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.


# rendering customer home page
@cust_login_required
def home(request):
    return render(request, "ecom/cust_home.html")


# Performing login operations for customer and reseller and
# rendering login page

def user_login(request):
    if request.method == 'POST':
        username = request.POST['userName']
        passwd = request.POST['userPassword']
        user = authenticate(username=username, password=passwd)
        if user is not None:
            login(request, user)
            try:
                # Login operation for customers
                customerdata = Customer.objects.get(login_id=user.id)
                request.session['customerid'] = user.id
                # if customer didn't complete otp verification send
                # otp and verifying it
                if customerdata.status == 'otpverify':
                    otp = randint(1000, 9999)
                    send_mail(
                        'please verify your otp',
                        str(otp),
                        'kiransurya032@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )
                    request.session['otpid'] = customerdata.login_id_id
                    Customer.objects.filter(login_id=user.id).update(otp=otp)
                    return redirect('verifyotp')
                # if customer already completed otp verification redirect
                # to home page
                else:
                    return redirect('home')
            except Customer.DoesNotExist:
                # Login operation for resellers
                resellerdata = Resellers.objects.get(login_id=user.id)
                request.session['resellerid'] = user.id
                # if Reseller didn't complete otp verification send
                #  otp and verifying it
                if resellerdata.status == 'otpverify':
                    # Generate otp and sending to mail
                    otp = randint(1000, 9999)
                    send_mail(
                        'please verify your otp',
                        str(otp),
                        'kiransurya032@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )
                    request.session['otpid'] = resellerdata.login_id_id
                    Resellers.objects.filter(login_id=user.id).update(otp=otp)
                    return redirect('verifyotp')
                # if Reseller already completed otp verification
                # redirect to home page
                else:
                    return redirect('/reseller/addProducts')
        # If credentials are wrong, paasing a error message
        else:
            return render(request, 'ecom/login.html', {'error': 'Invalid user details'})
    else:
        return render(request, "ecom/login.html")


def signup(request):
    # Perform signup operations if method = POST
    if request.method == "POST":
        # Read common information for customer and reseller
        usertype = request.POST['usertype']
        address = request.POST['address']
        country = request.POST['country']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        # Generate otp and sending to mail
        otp = randint(1000, 9999)
        send_mail(
                'please verify your otp',
                str(otp),
                'kiransurya032@gmail.com',
                [email],
                fail_silently=False,
            )
        if usertype == 'customer':
            # Read customer specific information and signing up
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            gender = request.POST['gender']
            dateofbirth = request.POST['dateofbirth']
            newuser = User.objects.create_user(email, email, password)
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.save()
            customerdata = Customer(firstname=firstname,gender=gender, mobile=mobile, dateofbirth=dateofbirth, address=address, country=country, user_type_id=1, login_id_id=newuser.id, status='otpverify', otp=str(otp))
            customerdata.save()
            user = User.objects.get(username=email)
            request.session['otpid'] = user.id
            request.session['customerid'] = user.id
            return redirect('verifyotp')
        else:
            # Read reseller specific information and signing up
            resellercompanyname = request.POST['resellercompanyname']
            resellercompanyid = request.POST['resellercompanyid']
            resellerbankaccountname = request.POST['resellerbankaccountname']
            resellerbankaccountnumber = request.POST['resellerbankaccountnumber']
            resellerbankaccountifsc = request.POST['resellerbankaccountifsc']
            newuser = User.objects.create_user(email, email, password)
            newuser.save()
            resellerdata = Resellers(companyname=resellercompanyname, companyregid=resellercompanyid, address=address, country=country, mobile=mobile, bankaccountholder=resellerbankaccountname, bankacccountnumber=resellerbankaccountnumber, bankacccountifsc=resellerbankaccountifsc, user_type_id=2, login_id_id=newuser.id, status='otpverify', otp=str(otp))
            resellerdata.save()
            user = User.objects.get(username=email)
            request.session['otpid'] = user.id
            request.session['resellerid'] = user.id
            return redirect('verifyotp')
    # Rendering signup page
    else:
        return render(request, "ecom/signup.html")


# Rendering search product page
def search_products(request):
    return render(request, "ecom/search_products.html")


# Rendering Product view page
def view_product(request):
    return render(request, "ecom/view_product.html")


# OTP verification
def verifyotp(request):
    # Verifying otp if method POST
    if request.method == "POST":
        id = request.session['otpid']
        otp = request.POST['inp_otp']
        try:
            userdata = Customer.objects.get(login_id_id=id)
            # Verifying OTP in customer table
            if(otp == userdata.otp):
                Customer.objects.filter(login_id_id=id).update(status='active')
                return redirect('/ecom/home')
            else:
                return render(request, "ecom/verify_otp.html", {"msg": "Invalid otp"})
        except Customer.DoesNotExist:
            userdata = Resellers.objects.get(login_id_id=id)
            # Verifying OTP in reseller table
            if(otp == userdata.otp):
                Resellers.objects.filter(login_id_id=id).update(status='inactive')
                return redirect('/reseller/home')
            else:
                return render(request, "ecom/verify_otp.html", {"msg": "Invalid otp"})
    # Rendering otp verification page
    else:
        return render(request, "ecom/verify_otp.html")


# Sending otp for change password
@csrf_exempt
def changepassword(request):
    if request.method == 'POST':
        username = request.POST['usrname']
        try:
            user = User.objects.get(username=username)
            try:
                # Send otp to customers for changing password
                custdata = Customer.objects.filter(login_id_id=user.id)
                otp = randint(1000, 9999)
                send_mail(
                        'please verify your otp',
                        str(otp),
                        'kiransurya032@gmail.com',
                        [username],
                        fail_silently=False,
                    )
                custdata.update(otp=otp)
            except Customer.DoesNotExist:
                # Send otp to Resellers for changing password
                reseldata = Resellers.objects.filter(login_id_id=user.id)
                otp = randint(1000, 9999)
                send_mail(
                        'please verify your otp',
                        str(otp),
                        'kiransurya032@gmail.com',
                        [username],
                        fail_silently=False,
                    )
                reseldata.update(otp=otp)
            # Return OTP send successfull message with a status
            return JsonResponse({'message': 'OTP send to your email, Please verify it', 'status': 'success', 'userid': username})
        except User.DoesNotExist:
            # Return OTP send Failed message with a status
            return JsonResponse({'message': 'Invalid username', 'status': 'failed'})
    # Render otp verification page
    else:
        return render(request, "ecom/forgotpassword.html")


# Changing password based on the otp verification
@csrf_exempt
def changepass(request):
    username = request.POST['usrname']
    password = request.POST['password']
    otp = request.POST['otp']
    user = User.objects.get(username=username)
    try:
        # Verifying customer otp and changing password
        custdata = Customer.objects.get(login_id_id=user.id)
        if otp == custdata.otp:
            user.set_password(password)
            user.save()
            # return redirect('login')
            return JsonResponse({"message": 'Your password changed successfully', "status": 'success'})
        else:
            # return redirect('changepassword')
            return JsonResponse({"message": 'Incorrect OTP', "status": 'false'})
    except Customer.DoesNotExist:
        # Verifying Reseller otp and changing password
        reseldata = Resellers.objects.get(login_id_id=user.id)
        if otp == reseldata.otp:
            user.set_password(password)
            user.save()
            # return redirect('login')
            return JsonResponse({"message": 'Your password changed successfully', "status": 'success'})
        else:
            # return redirect('changepassword')
            return JsonResponse({"message": 'Incorrect OTP', "status": 'false'})


def logout_view(request):
    logout(request)
    return redirect('/ecom/home')


def view_profile(request):
    id = request.session['customerid']
    logindata = User.objects.get(id=id)
    userdata = Customer.objects.get(login_id_id=id)
    return render(request, 'ecom/cust_profile.html', {'profiledata': userdata, 'userdata': logindata})


@csrf_exempt
def cust_change_password(request):
    if request.method == 'POST':
        id = request.session['customerid']
        user = User.objects.get(id=id)
        print(id)
        password = request.POST['password']
        print(password)
        otp = request.POST['otp']
        print(otp)
        customerdata = Customer.objects.get(login_id_id=id)
        if otp == customerdata.otp:
            user.set_password(password)
            user.save()
            # return redirect('login')
            return JsonResponse({"message": 'Your password changed successfully', "status": 'success'})
        else:
            return JsonResponse({"message": 'OTP is incorrect', "status": 'failed'})
    else:
        id = request.session['customerid']
        userdata = User.objects.get(id=id)
        otp = randint(1000, 9999)
        send_mail(
            'OTP for reset password in cs ecommerce application',
            str(otp),
            'kiransurya032@gmail.com',
            [userdata.email],
            fail_silently=False,
        )
        Customer.objects.filter(login_id_id=id).update(otp=otp)
        return render(request, "ecom/customer_chagepass.html", {"msg": "OTP send to your registred email id. Please verify..."})


@csrf_exempt
def custupdateprofile(request):
    fname = request.POST['firstname']
    lname = request.POST['lastname']
    address = request.POST['address']
    country = request.POST['country']
    mobile = request.POST['mobile']
    id = request.session['customerid']
    User.objects.filter(id=id).update(first_name=fname, last_name=lname)
    Customer.objects.filter(login_id_id=id).update(firstname=fname, mobile=mobile, address=address, country=country,)
    custdata = Customer.objects.get(login_id_id=id)
    customerdata = [{'firstname': custdata.firstname, 'gender': custdata.gender, 'dateofbirth': custdata.dateofbirth, 'mobile': custdata.mobile, 'address': custdata.address, 'country': custdata.country}]
    print(customerdata)
    userdata = User.objects.get(id=id)
    return JsonResponse({"custdata": customerdata})
