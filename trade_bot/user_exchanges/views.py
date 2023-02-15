from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Exchanges,PairTable,BinanceKeys1,BitmexKeys1,GateIoKeys1,KucoinKeys1,\
    Binance_model,Bitmex_model,Gate_model,Kucoin_model,Exception,Fills
from .serializer import BinanceSerial,BitmexSerial,GateSerial,\
    KucoinSerial,ExceptionSerial,Fillserial,ExchangesSeial,PairSerial,\
    BinanceKeysSerial,BitmexKeysSerial,GatekeySerial,KucoinKeysSerial
from scheduler_ import Stb
import jwt
from django.conf import settings
from rest_framework import status
import json
KEYS = getattr(settings, "KEY_", None)

class Binance_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()

        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            if data_.get('id') is not None:
                try:
                    bin=Binance_model.objects.get(username=data_.get('id'))
                except:
                    return Response({'status':False,'message':'data does not exists'},status=status.HTTP_404_NOT_FOUND)
                binserial=BinanceSerial(bin)
                return Response({'status':True,'data':binserial.data},status=status.HTTP_200_OK)
            else:
                bin=Binance_model.objects.all()
                binserial=BinanceSerial(bin,many=True)
                return Response({'status':True,'data':binserial.data},status=status.HTTP_200_OK)
        else:
            id=User.objects.get(username=uname).id
            try:
                bin = Binance_model.objects.get(username=id)
            except:
                return Response({'status': False, 'message': 'data not exists'}, status=status.HTTP_404_NOT_FOUND)
            binserial = BinanceSerial(bin)
            return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)



    def post(self,request,format=None):
        data_ = request.data
        token=request.META.get('HTTP_AUTHORIZATION')
        print(token)
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_400_BAD_REQUEST)


        if data_.get('status')=='True':
            obj = BinanceSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Binance data saved successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            data_ = request.data
            obj = ExceptionSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':False,'message':'ApiException saved','exchange_name':'Binance'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':False,'message':obj.errors,'exchange_name':'Binance'},status=status.HTTP_400_BAD_REQUEST)
class Bitmex_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
        uname = d.get('username')
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            if data_.get('id') is not None:
                try:
                    bit = Bitmex_model.objects.get(username=data_.get('id'))
                except:
                    return Response({'status': False, 'message': 'data does not exists'},
                                    status=status.HTTP_404_NOT_FOUND)
                bitserial = BitmexSerial(bit)
                return Response({'status': True, 'data': bitserial.data}, status=status.HTTP_200_OK)
            else:
                bit = Bitmex_model.objects.all()
                bitserial = BitmexSerial(bit, many=True)
                return Response({'status': True, 'data': bitserial.data}, status=status.HTTP_200_OK)
        else:
            id = User.objects.get(username=uname).id
            try:
                bin = Bitmex_model.objects.get(username=id)
            except:
                return Response({'status': False, 'message': 'data not exists'}, status=status.HTTP_404_NOT_FOUND)
            binserial = BitmexSerial(bin)
            return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_ = request.data
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])

        except:
            return Response({'status': False, 'message': 'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)

        status_ = data_.get('status')
        if status_=='True':
            obj = BitmexSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Bitmex Data Saved Successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            data_ = request.data
            obj = ExceptionSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':False,'message':'ApiException saved','exchange_name':'Bitmex'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':False,'message':obj.errors,'exchange_name':'Bitmex'},status=status.HTTP_400_BAD_REQUEST)

class Kucoin_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
        uname = d.get('username')
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            if data_.get('id') is not None:
                try:
                    bin = Kucoin_model.objects.get(username=data_.get('id'))
                except:
                    return Response({'status': False, 'message': 'data does not exists'},
                                    status=status.HTTP_404_NOT_FOUND)
                binserial = KucoinSerial(bin)
                return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
            else:
                bin = Kucoin_model.objects.all()
                binserial = KucoinSerial(bin, many=True)
                return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
        else:
            id_ = User.objects.get(username=uname).id
            try:
                bin = Kucoin_model.objects.get(id=id_)
            except:
                return Response({'status': False, 'message': 'data not exists'}, status=status.HTTP_404_NOT_FOUND)
            binserial = KucoinSerial(bin)
            return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)

    def post(self,request,format=True):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)

        status_ = data_.get('status')
        if status_=='True':
            obj = KucoinSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Kucoin Data Saved Successfully'
                                 ,'exchange_name':'Kucoin'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors ,'exchange_name':'Kucoin'},status=status.HTTP_400_BAD_REQUEST)
        else:
            data_ = request.data
            obj = ExceptionSerial(data=data_)

            if obj.is_valid():
                obj.save()
                return Response({'status':False,'message':'ApiException saved','exchange_name':'Kucoin'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':False,'message':obj.errors ,'exchange_name':'Kucoin'},status=status.HTTP_400_BAD_REQUEST)

class Gate_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)

        uname = d.get('username')
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            if data_.get('id') is not None:
                try:
                    bin = Gate_model.objects.get(id=data_.get('id'))
                except:
                    return Response({'status': False, 'message': 'data does not exists'},
                                    status=status.HTTP_404_NOT_FOUND)
                binserial = GateSerial(bin)
                return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
            else:
                bin = Gate_model.objects.all()
                binserial = GateSerial(bin, many=True)
                return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
        else:
            id_ = User.objects.get(username=uname).id
            try:
                bin = Gate_model.objects.get(id=id_)
            except:
                return Response({'status': False, 'message': 'data not exists'}, status=status.HTTP_404_NOT_FOUND)
            binserial = GateSerial(bin)
            return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_ = request.data
        print(token)
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'token Expired'},status=status.HTTP_401_UNAUTHORIZED)

        status_ = data_.get('status')
        if status_=='True':
            obj = GateSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Gate.io Data Saved Successfully',
                                 'exchange_name':'Gate.io'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors,'exchange_name':'Gate.io'},status=status.HTTP_400_BAD_REQUEST)
        else:
            data_ = request.data
            obj = ExceptionSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':False,'message':'ApiException saved','exchange_name':'Gate.io'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':False,'message':obj.errors,'exchange_name':'Gate.io'},status=status.HTTP_400_BAD_REQUEST)

class Fills_api(APIView):
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_=request.data
        print(token)
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'},status=status.HTTP_400_BAD_REQUEST)

        obj=Fillserial(data=data_)
        if obj.is_valid():
            obj.save()
            return Response({'status':True,'message':'Fills Data saved successfull','exchange_name':'Binance'},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':obj.errors,'exchange_name':'Binance'},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,pk=None,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        client_order_id=pk  
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        email = d.get('email')
        role = User.objects.get(email=email).role
        if role == '1':
            if pk is not None:
                client_order_id=str(client_order_id)
                client_order_id=str(client_order_id[client_order_id.find('=')+2:len(client_order_id)-1])
                obj=Fills.objects.filter(clientOrderId=str(client_order_id))
                print(obj)
                serial=Fillserial(obj,many=True)
                return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
            obj=Fills.objects.all()

            serial=Fillserial(obj,many=True)
            return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':"You are not an admin"},status=status.HTTP_401_UNAUTHORIZED)

class Bot_api(APIView):
    def post(self,request,format=None):
        data_=request.data
        token=request.META.get('HTTP_AUTHORIZATION')
        User=get_user_model()
        try:
            data=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:

            return Response({'status': False, 'message': 'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = data.get('username')
        id = User.objects.get(username=uname).id
        exc=Exchanges.objects.filter(status=1)
        exc=ExchangesSeial(exc,many=True)
        exchanges={"Exchanges":[]}
        lst=[]
        for i in exc.data:
            exchanges["Exchanges"].append({"exchange_name":i.get('exchange_name'),"Symbol":i.get('Symbol'),
                                           "api":i.get('api'),"socket":i.get('socket')})
            lst.append(i.get('exchange_name'))
        exchanges = json.dumps(exchanges)
        with open(r'config.json','w') as fl:
            fl.write(exchanges)

        if 'Binance' in lst:
            try:
                binkeys = BinanceKeys1.objects.get(id=id)
                binapi_key = binkeys.api_key
                binsecret_key = binkeys.secret_key

            except:
                return Response({'status': False, 'message': 'Binance keys  are not there'},status=status.HTTP_404_NOT_FOUND)
            try:
                bin_socket = Exchanges.objects.get(exchange_name='Binance').socket
            except:
                return Response({'status':False,'message':'Binance sockets are not there'},status=status.HTTP_404_NOT_FOUND)
        else:
            binapi_key = None
            binsecret_key = None
            bin_socket = None

        if 'Bitmex' in lst:
            try:
                bitkeys = BitmexKeys1.objects.get(id=id)
                bitapi_key = bitkeys.api_key
                bitsecret_key = bitkeys.secret_key

            except:
                return Response({'status': False, 'message': 'Bitmex keys are not there'},status=status.HTTP_404_NOT_FOUND)
            try:
                bit_socket = Exchanges.objects.get(exchange_name='Bitmex').socket
            except:
                return Response({'status':False,'message':'Bitmex Socket are not there'},status=status.HTTP_404_NOT_FOUND)
        else:
            bitapi_key = None
            bitsecret_key = None
            bit_socket = None
        if 'GateIo' in lst:
            try:
                gatekeys = GateIoKeys1.objects.get(id=id)
                gateapi_key = gatekeys.api_key
                gatesecret_key = gatekeys.secret_key

            except:
                return Response({'status': False, 'message': 'GateIo keys are not there'},status=status.HTTP_404_NOT_FOUND)
            try:
                gate_socket = Exchanges.objects.get(exchange_name='GateIo').socket
            except:
                return Response({'status':False,'message':'GateIo socket are not there'},status=status.HTTP_404_NOT_FOUND)
        else:
            gateapi_key = True
            gatesecret_key = True
            gate_socket = None

        if 'Kucoin' in lst:
            try:
                kuckeys = KucoinKeys1.objects.get(id=id)
                kucapi_key = kuckeys.api_key
                kucsecret_key = kuckeys.secret_key
                kucpassphrase = kuckeys.passphrase

            except:
                return Response({'status': False, 'message': 'Kucoin keys are not there '},status=status.HTTP_404_NOT_FOUND)
            try:
                kuk_socket = Exchanges.objects.get(exchange_name='Kucoin').socket
            except:
                return Response({'status':False,'message':'Kucoin socket are not there'},status=status.HTTP_404_NOT_FOUND)
        else:
            kucapi_key = None
            kucsecret_key = None
            kucpassphrase = None
            kuk_socket = None
        symbol=data_.get('symbol')
        amount=data_.get('amount')
        running=True
        print(id, symbol, token, amount, binapi_key, binsecret_key, bitapi_key, bitsecret_key, gateapi_key,
              gatesecret_key, kucapi_key, kucsecret_key, kucpassphrase)
        Stb(running,symbol, amount, token, id, binapi_key, binsecret_key, bitapi_key, bitsecret_key, gateapi_key,
            gatesecret_key, kucapi_key, kucsecret_key, kucpassphrase, bin_socket, bit_socket, gate_socket,
            kuk_socket)
        return Response({'status': True, 'message': 'Bot execution competed'},status=status.HTTP_200_OK)

class ConfigApi(APIView):
    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        email = d.get('email')
        role = User.objects.get(email=email).role
        if role == '1':
            obj=Exchanges.objects.all()
            serial=ExchangesSeial(obj,many=True)
            del obj
            return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':"You are not an admin"},status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User=get_user_model()
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        email=d.get('email')
        role=User.objects.get(email=email).role
        print(data_)
        if str(role) == '1':
            exchange_name=data_.get('exchange_name')
            print(exchange_name)
            if exchange_name is not None:
                try:
                    usr=Exchanges.objects.get(exchange_name=exchange_name)
                    print(usr.status)
                except:
                    return Response({'status':False,'message':'exchange_name is not avaliable'},status=status.HTTP_400_BAD_REQUEST)
                if usr.status=='0':
                    usr.status='1'
                    usr.save()
                    return Response({'status':True,'message':'Exchange Enable successfully'},status=status.HTTP_200_OK)
                else:
                    usr.status = '0'
                    usr.save()
                    return Response({'status': True, 'message': 'Exchange Disable successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':'No exchange provided'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'Only admins are allowed'},status=status.HTTP_401_UNAUTHORIZED)



class Set_Exchanges(APIView):


    def post(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User=get_user_model()
        email = d.get('email')
        role = User.objects.get(email=email).role
        if role=='1':
            serial=ExchangesSeial(data=data_)
            if serial.is_valid():
                serial.save()
                return Response({'status':True,'message':'Exchange data saved successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':serial.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)

class PairApi(APIView):
    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_=request.data
        print(data_)
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)

        obj=PairTable.objects.all()
        serial=PairSerial(obj,many=True)
        return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_=request.data

        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)

        User = get_user_model()
        email = d.get('email')

        role = User.objects.get(email=email).role

        if role=='1':
            serial=PairSerial(data=data_)
            if serial.is_valid():
                serial.save()
                return Response({'status':True,'message':'Pair saved successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':serial.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)

class SetBinanceKeys(APIView):
    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            id_= User.objects.get(username=uname).id
            obj = BinanceKeys1.objects.get(id=id_)
            serial = BinanceKeysSerial(obj)
            return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
    def post(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User=get_user_model()
        uname=d.get('username')
        id=User.objects.get(username=uname).id
        data_={'id':id,'api_key':data_.get('api_key'),'secret_key':data_.get('secret_key')}
        serial=BinanceKeysSerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status':True,'message':'Binance Keys Saved successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':serial.errors},status=status.HTTP_401_UNAUTHORIZED)

    def patch(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            id_=User.objects.get(username=uname).id
            #id_ = data_.get('id')
            print(id_)
            obj=BinanceKeys1.objects.get(id=id_)
            if data_.get('api_key') is not None:
                obj.api_key=data_.get('api_key')
            if data_.get('secret_key') is not None:
                obj.secret_key=data_.get('secret_key')
            obj.save()
            return Response({'status':True,'message':'data updated successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)



class SetBitmexKeys(APIView):
    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            id_ = User.objects.get(username=uname).id
            obj = BitmexKeys1.objects.get(id=id_)
            serial = BitmexKeysSerial(obj)
            return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])

        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        uname = d.get('username')
        id = User.objects.get(username=uname).id
        data_ = {'id': id, 'api_key': data_.get('api_key'), 'secret_key': data_.get('secret_key')}
        serial = BitmexKeysSerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status': True, 'message': 'Bitmex Keys Saved successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': serial.errors},status=status.HTTP_401_UNAUTHORIZED)

    def patch(self,request,format=None):
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
            id_=User.objects.get(username=uname).id
            obj=BitmexKeys1.objects.get(id=id_)
            obj=BitmexKeysSerial(obj,data=data_,partial=True)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Bitmex keys updated successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'You are not an Admin'},status=status.HTTP_401_UNAUTHORIZED)

class SetGateKeys(APIView):
    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            id_=User.objects.get(username=uname).id
            obj = GateIoKeys1.objects.get(id=id_)
            serial = GatekeySerial(obj)
            return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        uname = d.get('username')
        id = User.objects.get(username=uname).id
        data_ = {'id': id, 'api_key': data_.get('api_key'), 'secret_key': data_.get('secret_key')}
        serial = GatekeySerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status': True, 'message': 'GateIo Keys Saved successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': serial.errors},status=status.HTTP_401_UNAUTHORIZED)

    def patch(self,request,format=None):
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
            id_=User.objects.get(username=uname).id
            obj=GateIoKeys1.objects.get(id=id_)
            obj=GatekeySerial(obj,data=data_,partial=True)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Gate keys updated successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'You are not an Admin'},status=status.HTTP_401_UNAUTHORIZED)


class SetKucoinKeys(APIView):

    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            id_ = User.objects.get(username=uname)
            obj = KucoinKeys1.objects.get(id=id_)
            serial = KucoinKeysSerial(obj)
            return Response({'status':True,'data':serial.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)


    def post(self, request, format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'},status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        uname = d.get('username')
        id = User.objects.get(username=uname).id
        data_ = {'id': id, 'api_key': data_.get('api_key'), 'secret_key': data_.get('secret_key'),'passphrase':data_.get('passphrase')}
        serial = KucoinKeysSerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status': True, 'message': 'Kucoin Keys Saved successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': serial.errors},status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,format=None):
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
            id_=User.objects.get(username=uname).id
            obj=KucoinKeys1.objects.get(id=id_)
            obj=KucoinKeysSerial(obj,data=data_,partial=True)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Kucoin keys updated successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':obj.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'message':'You are not an Admin'},status=status.HTTP_401_UNAUTHORIZED)

class ExceptionAPI(APIView):
    def get(self,request,format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        User = get_user_model()
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
        uname = d.get('username')
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            if str(role) == '1':
                if data_.get('id') is not None:
                    try:
                        bin = Exception.objects.get(username=data_.get('id'))
                    except:
                        return Response({'status': False, 'message': 'data does not exists'},
                                        status=status.HTTP_404_NOT_FOUND)
                    binserial = ExceptionSerial(bin)
                    return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
                else:
                    bin = Exception.objects.all()
                    binserial = ExceptionSerial(bin, many=True)
                    return Response({'status': True, 'data': binserial.data}, status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'message':'You are not an admin'},status=status.HTTP_401_UNAUTHORIZED)
