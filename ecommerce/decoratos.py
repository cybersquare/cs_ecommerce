from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def cust_login_required(func):
    def wrap(request, *args, **kwargs):
        if not (request.session.get('customerid')):
            return redirect('/ecom/login')
        else:
            return func(request, *args, **kwargs)
    return wrap