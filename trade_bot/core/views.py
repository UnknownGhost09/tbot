from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializer import UserSerial
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
import jwt
import datetime
from datetime import  timedelta

from django.conf import settings
from rest_framework import status
KEYS = getattr(settings, "KEY_", None)
import public_ip as ip


class user_api(APIView):
    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()
        print(type(token))
        try:
            data=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)

        print('hello')
        username=data.get('username')
        obj=User.objects.filter(username=username)

        if len(obj)>0:
            usr=UserSerial(obj[0])
            usr=usr.data
            return Response({'status':True,'message':'Verified'},status=status.HTTP_200_OK)

        else:
            return Response({'status':False,'message':obj.errors},status=status.HTTP_400_BAD_REQUEST)
    def post(self,request,format=None):
        data_ = request.data
        token = request.META.get("HTTP-AUTHORIZATION")
        #token = data_.get('Authorization') #for own work

        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': "Token Expired"},status=status.HTTP_401_UNAUTHORIZED)

        User = get_user_model()
        uname=data_.get('username')
        password=make_password(data_.get('password'))
        fname=data_.get('first_name')
        lname=data_.get('last_name')
        em=data_.get('email')
        phone_no=data_.get('phone_no')

        created_at=data_.get('created_at')
        updated_at=data_.get('updated_at')
        email_verified_at=data_.get('email_verified_at')
        d={'username':uname,'password':password,'first_name':fname,
           'last_name':lname,'email':em,'phone_no':phone_no,
           'log_id':ip.get(),'created_at':created_at,'updated_at':updated_at,
           'email_verified_at':email_verified_at}
        obj = UserSerial(data=d)
        if obj.is_valid():
            obj.save()
            return Response({"status":True,'message':'data saved successfully'},status=status.HTTP_200_OK)
        return Response({"status":False, "message": obj.errors},status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request,format=None):
        data_=request.data
        User = get_user_model()
        id_=data_.get('id')
        if id_ is None:
            return Response({'status':False,'message':'No id is in data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            obj=User.objects.get(id=id_)
            usr=UserSerial(obj,data=data_)
            if usr.is_valid():
                usr.save()
                return Response({'status':True,'message':'data update successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':usr.errors},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status':False,'message':'not such user'},status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,format=None):
        data_ = request.data
        User = get_user_model()
        id_ = data_.get('id')
        if id_ is None:
            return Response({'status': False, 'message': 'No id is in data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            obj = User.objects.get(id=id_)
            usr = UserSerial(obj, data=data_,partial=True)
            if usr.is_valid():
                usr.save()
                return Response({'status': True, 'message': 'partial data update successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': usr.errors},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': False, 'message': 'not such user'},status=status.HTTP_400_BAD_REQUEST)

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
                request.session['name']=uname
                email_=user.email
                payload_ ={'email':email_,'username':uname,'exp':datetime.datetime.utcnow() + timedelta(days=30)}

                token = jwt.encode(payload=payload_,
                                   key=KEYS
                                   )
                return Response({'status': True, 'token':token ,'message':'Login Successfull','username':uname,'email':email_},status=status.HTTP_200_OK)
            email=User.objects.filter(email=uname)

            if len(email)>0:
                uname=email[0].username
                user = authenticate(request, username=uname, password=password)
                if user is not None:
                    email_= user.email
                    payload_ = {'email':email_,'username':uname,'exp':datetime.datetime.utcnow()+timedelta(days=30)}
                    token = jwt.encode(payload=payload_,key=KEYS)
                    return Response({'status': True, 'token': token,'message': 'Login Successfull','email':email_,'username':uname},status=status.HTTP_200_OK)
                else:
                    return Response({'status':False,'message':'email or password incorrect'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'status':False,'message':'username or password incorrect'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status':False,'message':'Please enter username and password'},status=status.HTTP_401_UNAUTHORIZED)
class LogOutApi(APIView):

    def post(self, request, format=None,):

        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            data = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            uname_ = data.get('username')
            email_ = data.get('email')
            payload_data = {'email': email_,'username':uname_,'exp':datetime.datetime.utcnow()+timedelta(microseconds=0.5)}
            token = jwt.encode(
                payload=payload_data,
                key=KEYS
            )
            return Response({'status':True,'message':'Logout Successfully'},status=status.HTTP_200_OK)
        except:
            return Response({'status':False,'message':'User already logout'},status=status.HTTP_400_BAD_REQUEST)

