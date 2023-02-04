from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Exchanges,PairTable,BinanceKeys,BitmexKeys,GateIoKeys,KucoinKeys
from .serializer import BinanceSerial,BitmexSerial,GateSerial,\
    KucoinSerial,ExceptionSerial,Fillserial,ExchangesSeial,PairSerial,\
    BinanceKeysSerial,BitmexKeysSerial,GatekeySerial,KucoinKeysSerial
from scheduler_ import Stb
import jwt
from django.conf import settings
from rest_framework import status
KEYS = getattr(settings, "KEY_", None)

class Binance_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})
    def post(self,request,format=None):
        data_ = request.data
        token=request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=settings.KEYS,algorithms=['HS256'])
            if data_.get('status')=='True':
                obj = BinanceSerial(data=data_)
                if obj.is_valid():
                    obj.save()
                    return Response({'status':True,'message':'Binance data saved successfully'})
                else:
                    return Response({'status':False,'message':obj.errors})
            else:
                data_ = request.data
                obj = ExceptionSerial(data=data_)
                if obj.is_valid():
                    obj.save()
                    return Response({'status':False,'message':'ApiException saved','exchange_name':'Binance'})
                else:
                    return Response({'status':False,'message':obj.errors,'exchange_name':'Binance'})
        except:
            return Response({'status':False,'message':'Token Expired'})

class Bitmex_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_ = request.data
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])

        except:
            return Response({'status': False, 'message': 'Token Expired'})
        status = data_.get('status')
        if status=='True':
            obj = BitmexSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Bitmex Data Saved Successfully'})
            else:
                return Response({'status':False,'message':obj.errors})
        else:
            data_ = request.data
            obj = ExceptionSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':False,'message':'ApiException saved','exchange_name':'Bitmex'})
            else:
                return Response({'status':False,'message':obj.errors,'exchange_name':'Bitmex'})

class Kucoin_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})

    def post(self,request,format=True):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'})
        status = data_.get('status')
        if status=='True':
            obj = KucoinSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Kucoin Data Saved Successfully'
                                 ,'exchange_name':'Kucoin'})
            else:
                return Response({'status':False,'message':obj.errors ,'exchange_name':'Kucoin'})
        else:
            data_ = request.data
            obj = ExceptionSerial(data=data_)

            if obj.is_valid():
                obj.save()
                return Response({'status':False,'message':'ApiException saved','exchange_name':'Kucoin'})
            else:
                return Response({'status':False,'message':obj.errors ,'exchange_name':'Kucoin'})

class Gate_api(APIView):
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_ = request.data
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'token Expired'})

        status = data_.get('status')
        if status=='True':
            obj = GateSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':True,'message':'Gate.io Data Saved Successfully',
                                 'exchange_name':'Gate.io'})
            else:
                return Response({'status':False,'message':obj.errors,'exchange_name':'Gate.io'})
        else:
            data_ = request.data
            obj = ExceptionSerial(data=data_)
            if obj.is_valid():
                obj.save()
                return Response({'status':False,'message':'ApiException saved','exchange_name':'Gate.io'})
            else:
                return Response({'status':False,'message':obj.errors,'exchange_name':'Gate.io'})

class Fills_api(APIView):
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_=request.data
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'})

        obj=Fillserial(data=data_)
        if obj.is_valid():
            obj.save()
            return Response({'status':True,'message':'Fills Data saved successfull','exchange_name':'Binance'})
        else:
            return Response({'status':False,'message':obj.errors,'exchange_name':'Binance'})

class Bot_api(APIView):
    def post(self,request,format=None):
        data_=request.data
        token=request.META.get('HTTP_AUTHORIZATION')
        User=get_user_model()
        try:
            data=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status': False, 'message': 'Token Expired'})
        exc=Exchanges.objects.filter(status=1)
        exc=ExchangesSeial(exc,many=True)
        exchanges={"Exchanges":[]}
        lst=[]
        for i in exc.data:
            exchanges["Exchanges"].append({"exchange_name":i.get('exchange_name'),"Symbol":i.get('Symbol'),
                                           "api":i.get('api'),"socket":i.get('socket')})
            lst.append(i.get('exchange_name'))
        with open(r'config.json','w') as fl:
            fl.write(exchanges)

        if 'Binance' in lst:
            try:
                binkeys = BinanceKeys.objects.get(id=id)
                binapi_key = binkeys.api_key
                binsecret_key = binkeys.secret_key
                bin_socket = Exchanges.objects.get(exchange_name='Binance').socket
            except:
                return Response({'status': False, 'message': 'Binance keys are not there or socket are not there'})
        else:
            binapi_key = None
            binsecret_key = None
            bin_socket = None

        if 'Bitmex' in lst:
            try:
                bitkeys = BitmexKeys.objects.get(id=id)
                bitapi_key = bitkeys.api_key
                bitsecret_key = bitkeys.secret_key
                bit_socket = Exchanges.objects.get(exchange_name='Bitmex').socket
            except:
                return Response({'status': False, 'message': 'Bitmex keys are not there or socket are not there'})
        else:
            bitapi_key = None
            bitsecret_key = None
            bit_socket = None
        if 'GateIo' in lst:
            try:
                gatekeys = GateIoKeys.objects.get(id=id)
                gateapi_key = gatekeys.api_key
                gatesecret_key = gatekeys.secret_key
                gate_socket = Exchanges.objects.get(exchange_name='GateIo').socket
            except:
                return Response({'status': False, 'message': 'GateIo keys are not there or socket are not there'})
        else:
            gateapi_key = True
            gatesecret_key = True
            gate_socket = None

        if 'Kucoin' in lst:
            try:
                kuckeys = KucoinKeys.objects.get(id=id)
                kucapi_key = kuckeys.api_key
                kucsecret_key = kuckeys.secret_key
                kucpassphrase = kuckeys.passphrase
                kuk_socket = Exchanges.objects.get(exchange_name='Kucoin').socket
            except:
                return Response({'status': False, 'message': 'Kucoin keys are not there or socket are not there'})
        else:
            kucapi_key = None
            kucsecret_key = None
            kucpassphrase = None
            kuk_socket = None
        symbol=data_.get('symbol')
        amount=data_.get('amount')

        print(id, symbol, token, amount, binapi_key, binsecret_key, bitapi_key, bitsecret_key, gateapi_key,
              gatesecret_key, kucapi_key, kucsecret_key, kucpassphrase)
        Stb(symbol, amount, token, id, binapi_key, binsecret_key, bitapi_key, bitsecret_key, gateapi_key,
            gatesecret_key, kucapi_key, kucsecret_key, kucpassphrase, bin_socket, bit_socket, gate_socket,
            kuk_socket)
        return Response({'status': True, 'message': 'Bot execution competed'})

class ConfigApi(APIView):
    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        User = get_user_model()
        email = d.get('email')
        role = User.objects.get(email=email).role
        if role == '1':
            obj=Exchanges.objects.all()
            serial=ExchangesSeial(obj,many=True)
            del obj
            return Response({'status':True,'data':serial.data})
        else:
            return Response({'status':False,'message':"You are not an admin"})

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
                    return Response({'status':True,'message':'Exchange Disable successfully'},status=status.HTTP_200_OK)
                else:
                    usr.status = '0'
                    usr.save()
                    return Response({'status': True, 'message': 'Exchange Enable successfully'},status=status.HTTP_200_OK)
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
            return Response({'status':False,'message':'Token Expired'})
        User=get_user_model()
        email = d.get('email')
        role = User.objects.get(email=email).role
        if role=='1':
            serial=ExchangesSeial(data=data_)
            if serial.is_valid():
                serial.save()
                return Response({'status':True,'message':'Exchange data saved successfully'})
            else:
                return Response({'status':False,'message':serial.error})
        else:
            return Response({"status":False,'message':'You are not an admin'})

class PairApi(APIView):
    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_=request.data
        print(data_)
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})

        obj=PairTable.objects.filter(pair=data_.get('pair'))
        serial=PairSerial(obj,many=True)
        return Response({'status':True,'message':serial.data})
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        data_=request.data
        print(data_)
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        print(d)
        User = get_user_model()
        email = d.get('email')

        role = User.objects.get(email=email).role

        if role=='1':
            serial=PairSerial(data=data_)
            if serial.is_valid():
                serial.save()
                return Response({'status':True,'message':'Pair saved successfully'})
            else:
                return Response({'status':False,'message':serial.errors})
        else:
            return Response({'status':False,'message':'You are not an admin'})

class SetBinanceKeys(APIView):
    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == ' 1':
            obj = BinanceKeys.objects.all()
            serial = BinanceKeysSerial(obj,many=True)
            return Response({'status':True,'message':serial.data})
        else:
            return Response({'status':False,'message':'You are not an admin'})
    def post(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        User=get_user_model()
        uname=d.get('username')
        id=User.objects.get(username=uname).id
        data_={'id':id,'api_key':data_.get('api_key'),'secret_key':data_.get('secret_key')}
        serial=BinanceKeysSerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status':True,'message':'Binance Keys Saved successfully'})
        else:
            return Response({'status':False,'message':serial.errors})

class SetBitmexKeys(APIView):
    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            obj = BinanceKeys.objects.all()
            serial = BinanceKeysSerial(obj,many=True)
            return Response({'status':True,'message':serial.data})
        else:
            return Response({'status':False,'message':'You are not an admin'})

    def post(self, request, format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])

        except:
            return Response({'status':False,'message':'Token Expired'})
        User = get_user_model()
        uname = d.get('username')
        id = User.objects.get(username=uname).id
        data_ = {'id': id, 'api_key': data_.get('api_key'), 'secret_key': data_.get('secret_key')}
        serial = BitmexKeysSerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status': True, 'message': 'Bitmex Keys Saved successfully'})
        else:
            return Response({'status': False, 'message': serial.errors})

class SetGateKeys(APIView):

    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            obj = BinanceKeys.objects.all()
            serial = BinanceKeysSerial(obj,many=True)
            return Response({'status':True,'message':serial.data})
        else:
            return Response({'status':False,'message':'You are not an admin'})

    def post(self, request, format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        User = get_user_model()
        uname = d.get('username')
        id = User.objects.get(username=uname).id
        data_ = {'id': id, 'api_key': data_.get('api_key'), 'secret_key': data_.get('secret_key')}
        serial = GatekeySerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status': True, 'message': 'GateIo Keys Saved successfully'})
        else:
            return Response({'status': False, 'message': serial.errors})

class SetKucoinKeys(APIView):

    def get(self,request,format=None):
        data_=request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d=jwt.decode(token,key=KEYS,algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        uname = d.get('username')
        User = get_user_model()
        role = User.objects.get(username=uname).role
        if str(role) == '1':
            obj = BinanceKeys.objects.all()
            serial = BinanceKeysSerial(obj,many=True)
            return Response({'status':True,'message':serial.data})
        else:
            return Response({'status':False,'message':'You are not an admin'})

    def post(self, request, format=None):
        data_ = request.data
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
        except:
            return Response({'status':False,'message':'Token Expired'})
        User = get_user_model()
        uname = d.get('username')
        id = User.objects.get(username=uname).id
        data_ = {'id': id, 'api_key': data_.get('api_key'), 'secret_key': data_.get('secret_key'),'passphrase':data_.get('passphrase')}
        serial = KucoinKeysSerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({'status': True, 'message': 'Kucoin Keys Saved successfully'})
        else:
            return Response({'status': False, 'message': serial.errors})
class BotTesting(APIView):
    def post(self,request,format=None):

        Stb('BTCUSDT', 0.5, 'abcdff', 1, 'ghjk', 'jkhjhj', 'hsdjfs', 'dsfhkjs', 'dfshjkf',
            'dsfksj', 'dfsjkl', 'dfksjf', 'dfsjhkfs','jklm','jfls','dfjks','fdsjkf')
        return Response({'status': True, 'message': 'Bot execution competed'})


