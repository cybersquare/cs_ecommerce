from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("hello cybersquare, welcome")
def home(request):
    return render(request,"ecom/index.html")