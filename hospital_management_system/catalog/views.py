from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from .models import Patient,Hospital,PatientVisit
from .serializers import PatientSerializer,HospitalSerializer,PatientVisitSerializer


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


