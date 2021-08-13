from os import stat
from django.core import serializers
from django.http import response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from common.models import TrainingModel


@csrf_exempt
@api_view(['GET', 'POST'])
def registerUser(request):
    if request.method=="POST":
        print("4444444test333333")
        userdetails= request.body
        firstname = userdetails['firstname']
        lastname = userdetails['lastname']
        username = userdetails['usertype']
        password = userdetails['password']
        try:
            userdata = TrainingModel.objects.get(username=username)
            resp = {"message": "User Already exist"}
        except:
            userdata = TrainingModel(firstname=firstname, lastname=lastname, username=username, password=password)
            userdata.save()
            resp = {'message': "User registred successfully"}
        return response(resp)
    else:
        print("4444444bad333333")
        return response(status=status.HTTP_400_BAD_REQUEST)