from django.shortcuts import render, redirect
from .models import Customer, User
from reseller.models import Resellers
from django.http.response import JsonResponse
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, "ecom/cust_home.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['userName']
        passwd = request.POST['userPassword']
        user = authenticate(username=username, password=passwd)
        if user is not None:
            try:
                customerdata = Customer.objects.get(login_id=user.id)
                request.session['customerid'] = user.id
                if customerdata.status == 'otpverify':
                    otp= randint(1000, 9999)
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
                else:
                    return redirect('home')
            except Customer.DoesNotExist:
                resellerdata = Resellers.objects.get(login_id=user.id)
                request.session['resellerid'] = user.id
                if resellerdata.status == 'otpverify':
                    otp= randint(1000, 9999)
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
                else:
                    return redirect('/reseller/addProducts')

        else:
            return render(request, 'ecom/login.html', {'error': 'Invalid user details'})
    else:
        return render(request, "ecom/login.html")


def signup(request):
    if request.method == "POST":
        usertype = request.POST['usertype']
        address = request.POST['address']
        country = request.POST['country']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        otp= randint(1000, 9999)

        send_mail(
                'please verify your otp',
                str(otp),
                'kiransurya032@gmail.com',
                [email],
                fail_silently=False,
            )
        if usertype == 'customer':
            # customer specific information
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            gender = request.POST['gender']
            dateofbirth = request.POST['dateofbirth']
            newuser = User.objects.create_user(email, email, password)
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.save()
            customerdata = Customer(firstname=firstname, gender=gender, mobile=mobile, dateofbirth=dateofbirth, address=address, country=country, user_type_id=1, login_id_id=newuser.id, status='otpverify', otp=str(otp))
            customerdata.save()
            user=User.objects.get(username=email)
            request.session['otpid'] = user.id
            request.session['customerid'] = user.id
            return redirect('verifyotp')
        else:
            # reseller specific information
            resellercompanyname = request.POST['resellercompanyname']
            resellercompanyid = request.POST['resellercompanyid']
            resellerbankaccountname = request.POST['resellerbankaccountname']
            resellerbankaccountnumber = request.POST['resellerbankaccountnumber']
            resellerbankaccountifsc = request.POST['resellerbankaccountifsc']
            newuser = User.objects.create_user(email, email, password)
            newuser.save()
            resellerdata = Resellers(companyname=resellercompanyname, companyregid=resellercompanyid, address=address, country=country, mobile=mobile, bankaccountholder=resellerbankaccountname, bankacccountnumber=resellerbankaccountnumber, bankacccountifsc=resellerbankaccountifsc, user_type_id=2, login_id_id=newuser.id, status='otpverify',otp=str(otp))
            resellerdata.save()
            user=User.objects.get(username=email)
            request.session['otpid'] = user.id
            request.session['resellerid'] = user.id
            return redirect('verifyotp')
    else:
        return render(request, "ecom/signup.html")


def search_products(request):
    return render(request, "ecom/search_products.html")


def view_product(request):
    return render(request, "ecom/view_product.html")


def verifyotp(request):
    if request.method == "POST":
        id=request.session['otpid']
        otp=request.POST['inp_otp']
        try:
            userdata=Customer.objects.get(login_id_id=id)
            if( otp==userdata.otp ):
                Customer.objects.filter(login_id_id=id).update(status='active')
                return redirect('/ecom/home')
            else:
                return render(request,"ecom/verify_otp.html", { "msg" : "Invalid otp" })
        except Customer.DoesNotExist:
            userdata=Resellers.objects.get(login_id_id=id)
            if( otp==userdata.otp ):
                Resellers.objects.filter(login_id_id=id).update(status='inactive')
                return redirect('/reseller/home')
            else:
                return render(request,"ecom/verify_otp.html", { "msg" : "Invalid otp" })
    else:
        return render(request,"ecom/verify_otp.html")

@csrf_exempt
def changepassword(request):
    if request.method == 'POST':
        username=request.POST['usrname']
        try:
            user=User.objects.get(username=username)
            try:
                custdata=Customer.objects.filter(login_id_id=user.id)
                otp= randint(1000, 9999)
                send_mail(
                        'please verify your otp',
                        str(otp),
                        'kiransurya032@gmail.com',
                        [username],
                        fail_silently=False,
                    )
                custdata.update(otp=otp)
            except Customer.DoesNotExist:
                reseldata=Resellers.objects.filter(login_id_id=user.id)
                otp= randint(1000, 9999)
                send_mail(
                        'please verify your otp',
                        str(otp),
                        'kiransurya032@gmail.com',
                        [username],
                        fail_silently=False,
                    )
                reseldata.update(otp=otp)
            return JsonResponse({'message': 'otp sent successfully','status' : 'success'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid username','status' : 'failed'})
    else:
        return render(request,"ecom/forgotpassword.html")

@csrf_exempt
def changepass(request):
    username=request.POST['usrname']
    password=request.POST['password']
    otp=request.POST['otp']
    user=User.objects.get(username=username)
    try:
        custdata=Customer.objects.get(login_id_id=user.id)
        if otp == custdata.otp:
            user.set_password(password)
            return JsonResponse({'message': "Password changed succesfully", 'status': 'true'})
        else:
            return JsonResponse({'message': "Invalid OTP", 'status': 'false'})
    except Customer.DoesNotExist:
        reseldata=Resellers.objects.get(login_id_id=user.id)
        if otp == reseldata.otp:
            user.set_password(password)
            return JsonResponse({'message': "Password changed succesfully", 'status': 'true'})
        else:
            return JsonResponse({'message': "Invalid OTP", 'status': 'false'})