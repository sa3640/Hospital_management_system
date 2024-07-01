from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,status
from rest_framework.decorators import api_view, action
from .models import Patient, Hospital, PatientVisit
from .serializers import PatientCreateSerializer,PatientVisitStatusSerializer,PatientVisitUpdateSerializer,PatientVisitDateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .helper import Patient_List_from_patentvisit,Patient_List_from_patient,LoginAPIView,SignupAPIView,CRUDHelper


# here we are checking we are checking if user is password is correct or not and tries to collect token 
class Login(LoginAPIView):
    pass

# here we are requesting user to signup which respond with token key
class Signup(SignupAPIView):
    pass

class Patient_Status_Patient_name(APIView):
    def get(self, request):
        CRUDHelper.model = PatientVisit
        CRUDHelper.serializer_class = PatientVisitStatusSerializer
        return CRUDHelper.get_all()

class PatientCreate(APIView):
    def post(self, request):
        CRUDHelper.model = Patient
        CRUDHelper.serializer_class = PatientCreateSerializer
        return CRUDHelper.create_instance(request.data)



class PatientVisitUpdate(APIView):
    def patch(self, request, contact_number):
        CRUDHelper.model = PatientVisit
        CRUDHelper.serializer_class = PatientVisitUpdateSerializer
        return CRUDHelper.update_instance(contact_number, request.data, partial=True)

class PatientVisitStatus(APIView):
    def get(self, request):
        CRUDHelper.model = PatientVisit
        CRUDHelper.serializer_class = PatientVisitDateSerializer
        return CRUDHelper.get_all()

class PatientInfo(APIView):
    def get(self,request):
        CRUDHelper.model = Patient
        CRUDHelper.serializer_class =   PatientCreateSerializer
        return CRUDHelper.get_patient()