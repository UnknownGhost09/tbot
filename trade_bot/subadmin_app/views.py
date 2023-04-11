from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from core.serializer import UserSerial
import jwt
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.conf import settings
KEYS = getattr(settings,'KEY_',None)
from rest_framework import status
from datetime import datetime

class SubAdminView(APIView):
    def post(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User=get_user_model
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname=d.get('username')
        role=User.objects.get(username=uname).role
        if str(role)=='2':
            User = get_user_model()
            uname = data_.get('username')
            password = make_password(data_.get('password'))
            fname = data_.get('first_name')
            lname = data_.get('last_name')
            em = data_.get('email')
            phone_no = data_.get('phone_no')
            log_id = data_.get('log_id')
            created_at = data_.get('created_at')
            #updated_at =
            email_verified_at = str(datetime.utcnow())
            d = {'username': uname, 'password': password, 'first_name': fname,
                 'last_name': lname, 'email': em, 'phone_no': phone_no,
                 'log_id': log_id, 'created_at': created_at,
                 'email_verified_at': email_verified_at,'role':'3'}
            obj = UserSerial(data=d)
            if obj.is_valid():
                obj.save()
                return Response({"status": True, 'message': 'Subadmin created successfully'},status=status.HTTP_200_OK)
            return Response({"status": False, "message": obj.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'only admin can register here'},status=status.HTTP_400_BAD_REQUEST)
