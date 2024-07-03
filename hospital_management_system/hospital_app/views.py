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
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from datetime import datetime


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
    permission_classes = [IsAuthenticated,IsAdminUser]
    
    
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


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

# 
     


class PatientVisitViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = PatientVisit.objects.all()
    serializer_class = PatientVisitSerializer

    
    
class PatientsByHospitalView(APIView):



    def get(self, request, hospital_name):
        try:
            hospital = Hospital.objects.get(name=hospital_name)
            patients = Patient.objects.filter(hospital=hospital)
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)
 


class DischargePatientView(APIView):
    def post(self, request, format=None):
        contact_number = request.data.get('contact_number')
        visit_date = request.data.get('hospital_visits')

        try:
            
            patient = Patient.objects.get(contact_number=contact_number)
            
            
            hospital = patient.hospital

            
            latest_visit, created = PatientVisit.objects.get_or_create(
                patient=patient,
                hospital=hospital,
                hospital_visits=visit_date,
                defaults={'patient_status': 'discharged'}
            )
            if not created:
                latest_visit.patient_status = 'discharged'
                latest_visit.hospital_visits = visit_date
                latest_visit.save()

            
            serializer = PatientVisitSerializer(latest_visit)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetPatientStatusByDateView(APIView):
    def get(self, request, format=None):
        contact_number = request.query_params.get('contact_number')
        date_str = request.query_params.get('date')

        if not contact_number or not date_str:
            return Response({'error': 'contact_number and date parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            date = datetime.strptime(date_str, '%Y-%m-%d')

            
            patient = Patient.objects.get(contact_number=contact_number)

            
            visits = PatientVisit.objects.filter(patient=patient, hospital_visits=date).order_by('-timestamp')

            if visits.exists():
                visit = visits.first()
                serializer = PatientVisitSerializer(visit)
                return Response(serializer.data)
            else:
                
                latest_visit = PatientVisit.objects.filter(patient=patient, hospital_visits__lte=date).order_by('-timestamp').first()
                if latest_visit:
                    serializer = PatientVisitSerializer(latest_visit)
                    return Response(serializer.data)
                else:
                    return Response({'error': 'No visit found for the given date'}, status=status.HTTP_404_NOT_FOUND)

        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)