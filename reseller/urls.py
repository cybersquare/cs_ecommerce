from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('reseller_home', views.reseller_home, name='reseller_home'),
    path('reseller_products', views.reseller_products, name= 'reseller_products'),
]