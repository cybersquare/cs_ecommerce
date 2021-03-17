from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('logout',views.logout_view, name="logout"),
    path('signup', views.signup, name='signup'),
    path('search_products', views.search_products, name='Search'),
    path('view_product/<int:id>', views.view_product, name='view'),
    path('verifyotp', views.verifyotp, name='verifyotp'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('changepass', views.changepass, name='changepass'),
    path('viewprofile', views.view_profile, name='viewprofile'),
    path('customer_changepassword', views.cust_change_password, name="customer_changepassword"),
    path('profile_update', views.custupdateprofile, name="profile_update"),
    path('addtobag', views.add_to_bag, name="addtobag"),
    path('viewBag', views.view_bag, name="viewBag"),
    path('updateQuantity', views.update_quantity, name="updateQuantity"),
    path('orderProduct', views.order_product, name='orderProduct'),
    path('updatePayment', views.updatepayment, name='updatePayment')
]
