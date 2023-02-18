from django.shortcuts import render
from rest_framework.views import APIView
from core.serializer import UserSerial
from .serializers import AppSerial
from .models import App_model
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
from .models import EmailModel,SmsModel
from .serializers import Email_serializer,Sms_serializer
from django.http import JsonResponse
class AdminView(APIView):
    def post(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname=d.get('username')
        role=User.objects.get(username=uname).role
        if str(role)=='1':
            uname = data_.get('username')
            password = make_password(data_.get('password'))
            fname = data_.get('first_name')
            lname = data_.get('last_name')
            em = data_.get('email')
            phone_no = data_.get('phone_no')
            role = data_.get('role')
            status_ = '1'
            created_at = data_.get('created_at')
            #updated_at = str(datetime.utcnow())
            email_verified_at = str(datetime.utcnow())
            d = {'username': uname, 'password': password, 'first_name': fname,
                 'last_name': lname, 'email': em, 'phone_no': phone_no,'status':status_,
                 'email_verified_at': email_verified_at,'role':role,'created_at':created_at}
            obj = UserSerial(data=d)
            if obj.is_valid():
                obj.save()
                if role=='2':
                    return Response({"status": True, 'message': 'subadmin created successfully'},status=status.HTTP_200_OK)
                else:
                    return Response({"status": True, 'message': 'user created successfully'},status=status.HTTP_200_OK)
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
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User=get_user_model()
        uname = d.get('username')
        try:
            user = User.objects.get(username=uname)
        except:
            return Response({'status':False,'msg': 'No user found'},status=status.HTTP_400_BAD_REQUEST)
        role = user.role
        if str(role) == '1':
            print(data_.get('id'))
            try:
                obj = User.objects.get(id=data_.get('id'))
            except:
                return Response({'status':False,'message':'No id in data'},status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'status':False,'message':'You can not update admin data'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': False, 'message': 'you are not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

class UsersData(APIView):

    def get(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
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
                             'total_pairs': len(pair.data), 'active_users': active},
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
            return Response({'status':False,'message':'Token Expired '},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            data_=request.data
            obj=AppSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'data saved successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'Status':False,'message':obj.errors},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
    def patch(self,request,format=None):
        data_=request.data
        print('app data',data_)
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        print('app_logo',data_.get('app_logo'))
        dic={'id':data_.get('values[id]'),'app_name':data_.get('values[app_name]'),'app_des':data_.get('values[app_des]'),'app_logo':data_.get('values[app_logo]'),'app_title':data_.get('values[app_title]'),'copyright':data_.get('values[copyright]')}
        if str(role) == '1':
            try:
                obj = App_model.objects.get(id=data_.get('values[id]'))
            except:
                return Response({'status':False,'message':'No app available'},status=status.HTTP_400_BAD_REQUEST)
            appserial = AppSerial(obj,data=data_, partial=True)
            if appserial.is_valid():
                appserial.update(obj,dic)
                return Response({'status': True, 'message': 'Data updated successfuly'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': appserial.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'message': 'you are not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role

        if str(role) == '1':
            obj=App_model.objects.all()
            app_serial=AppSerial(obj,many=True)

            return Response({'status':True,'app_data':app_serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'you are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
class PriceAPI(APIView):
    def post(self,request,format=None):
        data_=request.data
        symbol=data_.get('symbol')
        token=request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
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

        return Response({'status':True,'price':price},status=status.HTTP_200_OK)

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
                sub_admin=[{'id':i.get('id'),'username':i.get('username'),'first_name':i.get('first_name'),'last_name':i.get('last_name'),'created_at':i.get('created_at'),'email':i.get('email'),'phone_no':i.get('phone_no'),'status':i.get('status')} for i in sub_admin.data]
            else:
                sub_admin={}
            if len(usr.data)>0:
                usr=[{'id':i.get('id'),'username':i.get('username'),'first_name':i.get('first_name'),'last_name':i.get('last_name'),'created_at':i.get('created_at'),'email':i.get('email'),'phone_no':i.get('phone_no'),'status':i.get('status')} for i in usr.data]
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
                    return Response({'status':False,'message':'id is not available'},status=status.HTTP_400_BAD_REQUEST)
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

class Email_api(APIView):

    def patch(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            try:
                obj=EmailModel.objects.get(id=data_.get('id'))
            except:
                return Response({'status':True,'message':'No email available'},status=status.HTTP_400_BAD_REQUEST)
            if (data_.get('smtp_sever')==None) and (data_.get('mail_from')==None) and (data_.get('port')==None) and (data_.get('username')==None) and (data_.get('password')==None) and (data_.get('name')==None):
                return Response({'status':False,'message':'You cannot change the name field'},status=status.HTTP_400_BAD_REQUEST)
            emailserial=Email_serializer(obj,data=data_,partial=True)

            if emailserial.is_valid():
                emailserial.save()
                try:
                    with open(r'email.json', 'r') as fl:
                        d=fl.read()
                    d=json.loads(d)
                    if data_.get('id')==d.get('id'):
                        obj1=EmailModel.objects.get(id=data_.get('id'))
                        obj1=Email_serializer(obj1)
                        obj1=json.dumps(obj1.data)
                        with open(r'email.json','w') as fl:
                            fl.write(obj1)
                    else:
                        pass
                except:
                    pass
                return Response({'status':True,'message':'data updated successfuly'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'you are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
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
            obj=EmailModel.objects.filter(active_status='1')
            email_serial=Email_serializer(obj,many=True)

            return Response({'status':True,'email':email_serial.data},status=status.HTTP_200_OK)

        else:
            return Response({'status':False,'message':'you are not an admin'},status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            emailserial=Email_serializer(data=data_)
            if emailserial.is_valid():
                emailserial.save()
                return Response({'status':True,'message':'email data saved successfully'},status=status.HTTP_200_OK)
            else:
                obj = emailserial.errors
                return Response({'status':False,'message':list(obj.values())},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request,pk=None,format=None):

        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            try:
                obj=EmailModel.objects.get(name=data_.get('name'))
                obj.active_status='0'
                obj.save()
                try:
                    with open(r'email.json', 'r') as fl:
                        d=fl.read()
                    d=json.loads(d)
                    if data_.get('name')==d.get('name'):
                        with open(r'email.json','w') as fl:
                            fl.write("")
                    else:
                        pass
                except:
                    pass
                return Response({'status':True,'message':'email service deleted successfully'},status=status.HTTP_200_OK)
            except:
                return Response({'status':False,'message':'no email service avaliable'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status':False,'message':'You are not a admin'},status=status.HTTP_401_UNAUTHORIZED)
class Sms_api(APIView):

    def patch(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            try:
                obj=SmsModel.objects.get(id=data_.get('id'))
            except:
                return Response({'status':False,'message':'No data available'},status=status.HTTP_400_BAD_REQUEST)
            smsserial=Sms_serializer(obj,data=data_,partial=True)
            if smsserial.is_valid():
                smsserial.save()
                try:
                    with open(r'sms.json', 'r') as fl:
                        d=fl.read()
                    d=json.loads(d)
                    if data_.get('id')==d.get('id'):
                        obj1=SmsModel.objects.get(id=data_.get('id'))
                        obj1=Sms_serializer(obj1)
                        obj1=json.dumps(obj1.data)
                        with open(r'sms.json','w') as fl:
                            fl.write(obj1)
                    else:
                        pass
                except:
                    pass
                return Response({'status':True,'message':'Data updated successfuly'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':smsserial.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'you are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            try:
                obj=SmsModel.objects.get(name=data_.get('name'))
                obj.active_status='0'
                obj.save()
                try:
                    with open(r'sms.json', 'r') as fl:
                        d=fl.read()
                    d=json.loads(d)
                    if data_.get('name')==d.get('name'):
                        with open(r'sms.json','w') as fl:
                            fl.write("")
                    else:
                        pass
                except:
                    pass
                return Response({'status':True,'message':'sms service deleted successfully'},status=status.HTTP_200_OK)
            except:
                return Response({'status':False,'message':'no sms service avaliable'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status':False,'message':'You are not a admin'},status=status.HTTP_401_UNAUTHORIZED)
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
            obj=SmsModel.objects.filter(active_status='1')
            sms_serial=Sms_serializer(obj,many=True)
            return Response({'status':True,'email':sms_serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'you are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
    def post(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            smsserial=Sms_serializer(data=data_)
            if smsserial.is_valid():
                smsserial.save()
                return Response({'status':True,'message':'Sms data saved successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':smsserial.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
class SetEmail(APIView):
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
            try:
                with open(r'email.json','r') as fl:
                    data=fl.read()
                data=json.loads(data)
                return Response({'status':True,'data':data},status=status.HTTP_200_OK)
            except:
                return Response({'status':False},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
    def post(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            name=data_.get('name')
            try:
                obj=EmailModel.objects.get(name=name)
            except:
                return Response({'status':False,'message':'this email service is not available'},status=status.HTTP_400_BAD_REQUEST)
            emailserail=Email_serializer(obj)
            emailserail=json.dumps(emailserail.data)
            with open(r'email.json','w') as fl:
                fl.write(emailserail)
            return Response({'status':True,'message':str(name) + ' selected successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'you are not an admin'},status=status.HTTP_401_UNAUTHORIZED)


class SetSms(APIView):

    def get(self, request, format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            try:

                with open(r'sms.json', 'r') as fl:
                    data = fl.read()
                data = json.loads(data)
                return Response({'status': True, 'data': data}, status=status.HTTP_200_OK)
            except:
                return Response({'status': False},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'message': 'You are not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            name = data_.get('name')
            try:
                obj = SmsModel.objects.get(name=name)
            except:
                return Response({'status': False, 'message': 'this sms service is not avaliable'},
                                status=status.HTTP_400_BAD_REQUEST)
            smsserail = Sms_serializer(obj)
            smsserail = json.dumps(smsserail.data)
            with open(r'sms.json', 'w') as fl:
                fl.write(smsserail)
            return Response({'status': True, 'message': str(name) + ' selected successfully'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': 'you are not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

class Logs(APIView):
    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        id_ = User.objects.get(username=uname).id
        with open(r'tradedata.json','r') as fl:
            data=fl.read()
            data="["+data[1:]+"]"
        data=json.loads(data)
        lst=[i for i in data if i.get('id')==id_]
        return Response({'status':True,'data':lst })

