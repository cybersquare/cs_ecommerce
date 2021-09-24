from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('Ang_AllProducts', views.ang_view_product, name='Ang_AllProducts'),
    path('Ang_Signup', views.ang_signup, name="Ang_Signup"),
    path('otpVerify', views.otpVerification, name="otpVerify"),
    path('Ang_Login', views.ang_Login, name="Ang_Login"),
    path('RegisterUser', views.registerUser, name="RegisterUser"),
    path('GetResProducts', views.get_res_products, name="GetResProducts"),
    path('ResellersApproval', views.approveReseller, name="ResellersApproval"),
    path('Profiledetails', views.AngProfileView, name="Profiledetails"),
    path('resellerVerification', views.AngVerifyReseller, name="resellerVerification"),
    path('AngAllResellers', views.AngViewReseller, name="AngAllResellers"),
    path('AngAdminLogin', views.AngAdminLogin, name="AngAdminLogin"),
    path('AngAddProduct', views.ResAddProduct, name="AngAddProduct"),
    path('searchProducts', views.search_products, name="searchProducts"),
    path('ProductView', views.Ang_view_product, name="ProductView"),
    path('resDeleteProducts',views.resDeleteProducts, name="reseleteProducts"),
    path('resUpdateProducts',views.resUpdateProducts, name="resUpdateProducts"),
    path('ProductAddToCart',views.Ang_addToCart, name="ProductAddToCart"),
    path('AngViewCart',views.AngViewCart, name="AngViewCart"),
    path('changePassword', views.changepassword, name="changePassword"),
    path('createOrder', views.createOrder, name="createOrder"),
    path("PlaceOrder", views.PlaceOrder, name="PlaceOrder"),
    path("viewOrders", views.viewOrders, name="viewOrders"),
    path('AngEditProfile', views.AngEditProfile, name="AngEditProfile"),
]