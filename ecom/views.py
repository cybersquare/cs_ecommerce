from django.shortcuts import render, redirect
from .models import Customer, User
from reseller.models import Resellers
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.

def home(request):
    return render(request, "ecom/cust_home.html")


def login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['userName']
        print(username)
        passwd = request.POST['password']
        print(passwd)

        user = authenticate(username=username, password=passwd)
        if user is not None:
            try:
                customerdata = Customer.objects.get(login_id=user.id)
                request.session['customerid'] = user.id
                return redirect('home')
            except Customer.DoesNotExist:
                return redirect('/reseller/home')

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
# customer specific information
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST['gender']
        dateofbirth = request.POST['dateofbirth']
# reseller specific information
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
            customerdata = Customer(firstname=firstname, gender=gender, mobile=mobile, dateofbirth=dateofbirth, address=address, country=country, user_type_id=1, login_id_id=newuser.id)
            customerdata.save()
            return redirect('login')
        else:
            newuser = User.objects.create_user(email, email, password)
            newuser.save()
            resellerdata = Resellers(companyname=resellercompanyname, companyregid=resellercompanyid, address=address, country=country, mobile=mobile, bankaccountholder=resellerbankaccountname, bankacccountnumber=resellerbankaccountnumber, bankacccountifsc=resellerbankaccountifsc, user_type_id=2, login_id_id=newuser.id)
            resellerdata.save()
            return redirect('login')
    else:
        return render(request, "ecom/signup.html")


def search_products(request):
    return render(request, "ecom/search_products.html")


def view_product(request):
    return render(request, "ecom/view_product.html")
