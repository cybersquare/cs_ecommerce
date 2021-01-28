from django.urls import path
from . import views

urlpatterns=[
    # path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('search_products',views.search_products,name='Search'),
    path('view_product',views.view_product,name='view'),

]