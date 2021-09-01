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
]