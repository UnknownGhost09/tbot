from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializer import BinanceSerial,BitmexSerial,GateSerial,KucoinSerial,ExceptionSerial,Fillserial
from scheduler_ import Stb

# Create your views here.
#in exception we send False in status
#Without Exception we send True in status

class Binance_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})

    def post(self,request,format=None):
        data_ = request.data
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


class Bitmex_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})

    def post(self,request,format=None):
        data_ = request.data
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
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})

    def post(self,request,format=True):
        data_ = request.data
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
                return Response({'status':False,'message':'ApiException saved' ,'exchange_name':'Kucoin'})
            else:
                return Response({'status':False,'message':obj.errors ,'exchange_name':'Kucoin'})

class Gate_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        data_ = request.data
        return Response({'status':True})

    def post(self,request,format=None):
        data_ = request.data
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
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        data_=request.data
        obj=Fillserial(data=data_)
        if obj.is_valid():
            obj.save()
            return Response({'status':True,'message':'Fills Data saved successfull','exchange_name':'Binance'})
        else:
            return Response({'status':False,'message':obj.errors,'exchange_name':'Binance'})


class Bot_api(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        data_=request.data
        id=data_.get('id')
        User = get_user_model()
        token = Token.objects.get(user=id)
        symbol=data_.get('symbol')
        amount=data_.get('amount')
        print(id,symbol,token,amount)
        Stb(symbol,amount,token,id)
        return Response({'status':True,'message':'Bot execution competed'})









