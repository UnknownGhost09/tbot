import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializer import UserSerial
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from rest_framework import authentication


class user_api(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        data_ = request.data
        User = get_user_model()
        uname=data_.get('username')
        password=make_password(data_.get('password'))
        fname=data_.get('first_name')
        lname=data_.get('last_name')
        em=data_.get('email')
        phone_no=data_.get('phone_no')
        log_id=data_.get('log_id')
        created_at=data_.get('created_at')
        updated_at=data_.get('updated_at')
        email_verified_at=data_.get('email_verified_at')
        d={'username':uname,'password':password,'first_name':fname,
           'last_name':lname,'email':em,'phone_no':phone_no,
           'log_id':log_id,'created_at':created_at,'updated_at':updated_at,
           'email_verified_at':email_verified_at}
        obj = UserSerial(data=d)
        if obj.is_valid():
            obj.save()
            return Response({"status":True,'msg':'data saved successfully'})
        return Response({"status":False, "msg": obj.errors})
    def put(self,request,format=None):
        data_=request.data
        User = get_user_model()
        id_=data_.get('id')
        if id_ is None:
            return Response({'status':False,'msg':'no id is in data'})
        try:
            obj=User.objects.get(id=id_)
            usr=UserSerial(obj,data=data_)
            if usr.is_valid():
                usr.save()
                return Response({'status':True,'msg':'data update successfully'})
            else:
                return Response({'status':False,'msg':usr.errors})
        except:
            return Response({'status':False,'msg':'not such user'})
    def patch(self,request,format=None):
        data_ = request.data
        User = get_user_model()
        id_ = data_.get('id')
        if id_ is None:
            return Response({'status': False, 'msg': 'no id is in data'})
        try:
            obj = User.objects.get(id=id_)
            usr = UserSerial(obj, data=data_,partial=True)
            if usr.is_valid():
                usr.save()
                return Response({'status': True, 'msg': 'partial data update successfully'})
            else:
                return Response({'status': False, 'msg': usr.errors})
        except:
            return Response({'status': False, 'msg': 'not such user'})


class Login(APIView):
    def post(self,request,format=None):
        data_=request.data
        uname= data_.get('username')
        password = data_.get('password')
        User = get_user_model()
        if uname is not None and password is not None:
            user = authenticate(request, username=uname, password=password)
            if user is not None:
                login(request,user)
                data_ = requests.post(url='http://127.0.0.1:8000/api/token/',
                                      data={'username': uname, 'password': password})
                data_ = data_.json()

                return Response({'status': True, 'token': data_, 'id': user.id,'role':user.role,'message':'Login Successfull'})
            email=User.objects.filter(email=uname)

            if len(email)>0:
                uname=email[0].username
                user = authenticate(request, username=uname, password=password)
                if user is not None:
                    login(request, user)
                    data_ = requests.post(url='http://127.0.0.1:8000/api/token/',
                                          data={'username': uname, 'password': password})
                    data_ = data_.json()

                    return Response({'status': True, 'token': data_, 'id': user.id, 'role': user.role,
                                     'message': 'Login Successfull'})
                else:
                    return Response({'status':False,'message':'email or password incorrect'})
            else:
                return Response({'status':False,'message':'username or password incorrect'})
        else:
            return Response({'status':False,'msg':'Please enter username and password'})
class LogOutApi(APIView):
    def post(self,request,format=None):
        logout(request)
        return Response({'status':True,'message':'Logout Successfully'})




