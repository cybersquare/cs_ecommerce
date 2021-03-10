from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from . import views
# from rest_framework.test import APIClient
# from rest_framework import status
# Create your tests here.


class TestReseller(TestCase):
    def test_login(self):
        # def setUp(self):
        # self.factory = RequestFactory()
        newuser = [
            {"userName": "rishaa@gmail.com", "password": "123"}
        ]
        url = reverse('login')
        print("&&&&&", url)
        res = self.client.post(url, newuser[0])
        # res = views.login(newuser)
        print("#######")
        print(res)
        self.assertEquals(res.status_code, 200)
        self.assertRedirects(
            response,
            expected_url="/reseller/home")
    #     data = {
    #         "usrname": "test",
    #         "passwd": "user"
    #     }
    #     url = reverse('login')
    #     res = self.client.get(url)
    #     print("seee here############")
    #     print(res.data)
    #     self.assertEquals(res.status_code, 200)
    # def test_login(self):
# testcases tested by user - id 2 & 3
# from .models import Customer
# from django.contrib.auth.models import User
# # Create your tests here.
# data_set = {
#     "setUp": [
#         { "firstName": "surya", "mobile":"9893456790","gender":"male","dateofbirth":"2000/12/05","address":'test abcd',"country":"india","status":"false","user_type":"customer","login_id":"15" },
#     ]
# }
# class MyTest(TestCase):
#     def setUp(self,req):
#         req_data = req["setUp"][0]
#         user = User.objects.get(id = req_data["login_id"])
#         self.assertEqual(user.first_name,"surya")
    # customer_obj = Customer.objects.create(firstname = req_data["firstName"],
    #                 mobile = req_data["mobile"], gender = req_data["gender"],
    #                 dateofbirth = req_data["dateofbirth"], address = req_data["address"],
    #                 country = req_data["country"], status = req_data["status"],
    #                 user_type = req_data["user_type"], login_id = req_data["login_id"])
# test = MyTest()
# test.setUp(data_set)
