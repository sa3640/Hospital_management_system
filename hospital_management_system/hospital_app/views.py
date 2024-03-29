from django.shortcuts import render

# Create your views here.


from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import api_view, action
from .models import Patient,Hospital,PatientVisit
from .serializers import PatientSerializer,HospitalSerializer,PatientVisitSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated





@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail" : "Not found"},status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token":token.key, "user":serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user":serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HospitalViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    
    @action(detail=True, methods=['post'])
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
class PatientViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    patient_separator = ","

    def get_queryset(self):

        contactnumber = self.request.query_params.get("contactnumber", None)

        if contactnumber:
            
            qs = Patient.objects.filter()
            for patient in contactnumber.split(self.patient_separator):
                qs = qs.filter(contact_number=patient)

                return qs

        return super().get_queryset()

    @action(detail=True,methods=['post'])
    def perform_create(self, serializer):
        return super().perform_create(serializer)  
    

# 
     


    
class PatientVisitViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



    queryset = PatientVisit.objects.all()
    serializer_class = PatientVisitSerializer

    patient_separator = ","

    def get_queryset(self):

        contactnumber = self.request.query_params.get("contactnumber", None)

        if contactnumber:
            
            qs = PatientVisit.objects.filter()
            for patient in contactnumber.split(self.patient_separator):
                qs = qs.filter(patient__contact_number=patient)

                return qs

        return super().get_queryset()


