from django.shortcuts import render
from rest_framework.views import APIView
from core.serializer import UserSerial
from core.serializer import AppSerial
import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import json
import requests
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
KEYS = getattr(settings,'KEY_',None)
from user_exchanges.serializer import ExchangesSeial,PairSerial
from user_exchanges.models import Exchanges,PairTable
import pandas as pd

class AdminView(APIView):
    def post(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)

        uname=d.get('username')
        role=User.objects.get(username=uname).role
        if str(role)=='1':

            uname = data_.get('username')
            password = make_password(data_.get('password'))
            fname = data_.get('first_name')
            lname = data_.get('last_name')
            em = data_.get('email')
            phone_no = data_.get('phone_no')
            role = '2'
            status_ = '1'
            created_at = str(datetime.utcnow())
            #updated_at = str(datetime.utcnow())
            email_verified_at = str(datetime.utcnow())
            d = {'username': uname, 'password': password, 'first_name': fname,
                 'last_name': lname, 'email': em, 'phone_no': phone_no,'status':status_,
                 'email_verified_at': email_verified_at,'role':role,'created_at':created_at}
            obj = UserSerial(data=d)
            if obj.is_valid():
                obj.save()
                return Response({"status": True, 'message': 'subadmin created successfully'})
            else:
                val=obj.errors
                return Response({"status": False, "message": list(val.values())},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'only admin can register here'},status=status.HTTP_401_UNAUTHORIZED)

    def patch(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        User=get_user_model()
        uname = d.get('username')
        try:
            user = User.objects.get(username=uname)
        except:
            return Response({'msg': 'No user found'})
        role = user.role
        if str(role) == '1':
            print(data_.get('id'))
            try:
                obj = User.objects.get(id=data_.get('id'))
            except:
                return Response({'status':False,'message':'no id in data'},status=status.HTTP_400_BAD_REQUEST)
            role=obj.role
            if role!='1':
                usr = UserSerial(obj, data=data_, partial=True)
                if usr.is_valid():
                    usr.save()
                    obj.updated_at=str(datetime.utcnow())
                    obj.save()
                    return Response({'status': True, 'message': 'User data updated successfully'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'message': usr.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':False,'message':'You can not update admin data'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'message': 'you are not an admin'}, status=status.HTTP_401_UNAUTHORIZED)



class UsersData(APIView):
    def get(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)

        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            User = get_user_model()
            obj = User.objects.all()
            user_serial = UserSerial(obj, many=True)
            df = pd.DataFrame(user_serial.data)
            df['date'] = df['created_at'].str[:10]
            grp1 = df.groupby('date').count()['id']
            grp2 = df.groupby('status').count()['id']
            grp1 = grp1.to_dict()
            grp2 = grp2.to_dict()
            active = grp2.get('1')
            if active is None:
               grp2['1']=0
            user_exchange = Exchanges.objects.all()
            user_exchange = ExchangesSeial(user_exchange, many=True)
            pair = PairTable.objects.all()
            pair = PairSerial(pair, many=True)
            return Response({'status': True, 'chart': {'date_joined': grp1}, 'total_users': len(df),
                             'Exchanges': user_exchange.data, 'total_exchanges': len(user_exchange.data),
                             'total_pairs': len(pair.data), 'pairs': pair.data, 'active_users': active},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': 'You are not admin'}, status=status.HTTP_401_UNAUTHORIZED)

class AppApi(APIView):
    parser_classes = [MultiPartParser,FormParser]
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)

        data_=request.data
        obj=AppSerial(data=data_,instance=request.user)
        if obj.is_valid():
            obj.save()
            return Response({'status':True,'message':'data saved successfully'})
        else:
            return Response({'Status':False,'message':obj.errors},status=status.HTTP_401_UNAUTHORIZED)


class PriceAPI(APIView):
    def post(self,request,format=None):
        data_=request.data
        symbol=data_.get('symbol')
        token=request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'})

        with open('price.json','r') as fl:
            URL=fl.read()
        URL=json.loads(URL)
        URL=URL.get('Symbol')
        price=requests.get(url=URL)
        price=pd.DataFrame(price)
        price=price.loc[price['symbol']==symbol,:]
        price=price.to_dict()
        price['price']=list(price.get('price').values())[0]
        price['symbol']=list(price.get('symbol').values())[0]
        return Response({'status':True,'price':price})


class UsersApi(APIView):
    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)

        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            sub_admin=User.objects.filter(role='2')
            usr=User.objects.filter(role='3')
            sub_admin=UserSerial(sub_admin,many=True)
            usr=UserSerial(usr,many=True)
            if len(sub_admin.data)>0:
                sub_admin=[{'id':i.get('id'),'username':i.get('username'),'first_name':i.get('first_name'),'last_name':i.get('last_name'),'date_joined':i.get('date_joined'),'email':i.get('email'),'phone_no':i.get('phone_no'),'status':i.get('status')} for i in sub_admin.data]
            else:
                sub_admin={}
            if len(usr.data)>0:
                usr=[{'id':i.get('id'),'username':i.get('username'),'first_name':i.get('first_name'),'last_name':i.get('last_name'),'date_joined':i.get('date_joined'),'email':i.get('email'),'phone_no':i.get('phone_no'),'status':i.get('status')} for i in usr.data]
            else:
                usr={}
            return Response({'status':True,'users':usr,'sub_admins':sub_admin},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)


class userInactiveApi(APIView):
    def post(self,request,format=None):
        data_=request.data
        token= request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            id=data_.get('id')
            if id is not None:
                try:
                    User=get_user_model()
                    usr=User.objects.get(id=id)
                    print(usr.status)
                except:
                    return Response({'status':False,'message':'id is not avaliable'},status=status.HTTP_400_BAD_REQUEST)
                if usr.status=='1':
                    usr.status='0'
                    usr.save()
                    usr.updated_at = str(datetime.utcnow())
                    usr.save()
                    return Response({'status':True,'message':'User Inactive successfully'},status=status.HTTP_200_OK)
                else:
                    usr.status = '1'
                    usr.save()
                    usr.updated_at = str(datetime.utcnow())
                    usr.save()
                    return Response({'status': True, 'message': 'User Active successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':'No id provided'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'Only admins can inactive any user or sub admin'},status=status.HTTP_401_UNAUTHORIZED)






