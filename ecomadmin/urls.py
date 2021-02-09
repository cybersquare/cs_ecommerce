from django.urls import path
from . import views

urlpatterns = [
    path('managereseller', views.mngreseller, name='managereseller'),
    path('addreseller', views.addreseller, name='addreseller'),
    path('deletereseller', views.deletereseller, name='deletereseller'),
    path('adminlogin', views.admlogin, name='adminlogin'),


]
