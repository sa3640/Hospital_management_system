from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from .models import Patient, Hospital, PatientVisit
from .serializers import PatientSerializer, HospitalSerializer, PatientVisitSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# here we are checking we are checking if user is password is correct or not and tries to collect token 
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

# here we are requesting user to signup which respond with token key
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HospitalViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class PatientViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    patient_separator = ","
# here we are fetching patient credential with his contact number
    def get_queryset(self):
        return self.filter_by_contact_number(super().get_queryset())

    def filter_by_contact_number(self, queryset):
        contactnumber = self.request.query_params.get("contactnumber", None)
        if contactnumber:
            for patient in contactnumber.split(self.patient_separator):
                queryset = queryset.filter(contact_number=patient)
        return queryset


class PatientVisitViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PatientVisit.objects.all()
    serializer_class = PatientVisitSerializer
    patient_separator = ","
 
 # here we are fetching patient status with his contact number
    def get_queryset(self):
        return self.filter_by_contact_number(super().get_queryset())

    def filter_by_contact_number(self, queryset):
        contactnumber = self.request.query_params.get("contactnumber", None)
        if contactnumber:
            for patient in contactnumber.split(self.patient_separator):
                queryset = queryset.filter(patient__contact_number=patient)
        return queryset