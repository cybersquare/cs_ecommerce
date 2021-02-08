from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('master', views.reseller_master, name='reseller_master'),
    path('home', views.reseller_home, name='reseller_home'),
    path('products', views.reseller_products, name='reseller_products'),
    path('addProducts', views.reseller_addProducts, name='reseller_addProducts'),
    # path('login',views.reseller_login,name='login'),
    # path('signup',views.reseller_signup,name='signup'),

]
