from django.urls import path
from . import views

urlpatterns = [
    path('Ang_AllProducts', views.ang_view_product, name='Ang_AllProducts'),
    path('Ang_Signup', views.ang_signup, name="Ang_Signup"),
    path('otpVerify', views.otpVerification, name="otpVerify")
]