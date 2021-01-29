from django.urls import path
from . import views

urlpatterns=[
    # path('', views.index, name='index'),
    # path('home', views.home, name='home'),
    # path('login',views.login,name='login'),
    path('managereseller',views.mngreseller,name='managereseller'),
    path('addreseller',views.addreseller,name='addreseller'),
    path('deletereseller',views.deletereseller,name='deletereseller'),
    path('adminlogin',views.admlogin,name='adminlogin'),
    

]