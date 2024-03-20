from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from .models import Patient,Hospital,PatientVisit,User
from .serializers import PatientSerializer,HospitalSerializer,PatientVisitSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class HospitalViewSet(viewsets.ModelViewSet):
    
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    
    @action(detail=True, methods=['post'])
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @action(detail=True,methods=['post'])
    def perform_create(self, serializer):
        return super().perform_create(serializer)  
    

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter()
    serializer_class = PatientSerializer

    @action(detail=True,methods=['post'])
    def perform_create(self, serializer):
        return super().perform_create(serializer)  


class PatientVisitViewSet(viewsets.ModelViewSet):
    queryset = PatientVisit.objects.all()
    serializer_class = PatientVisitSerializer


class RegisterUser(APIView):
    def post(request,self):
       serializer = UserSerializer(data = request.data)
       
       if not serializer.is_valid():
           return Response({'status': 403, 'errors' : serializer.errors, 'message' : 'something is not working'})
       
       serializer.save()

       user = User.objects.get(username = serializer.data['useername'])
       token_obj , _ = Token.objects.get_or_create(user=user)
       return Response ({'status': 200, 'payload' : serializer.data, 'token' : str(token_obj) , 'message' : 'Your data is saved'})