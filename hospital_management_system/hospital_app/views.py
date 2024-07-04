from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from .models import Patient,Hospital,PatientVisit
from .serializers import HospitalSerializer,PatientVisitSerializer,UserSerializer,PatientSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.utils.decorators import method_decorator
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


class HospitalCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self,request):
        serializer =  HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class HospitalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def get(self,request):
        hospital = Hospital.objects.all().values('id','name','address','staffs_num','num_of_beds')
        hospital_list = list(hospital)
        return JsonResponse(hospital_list,safe=False)
    
class DeleteHospital(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def delete(self,request,hospital_name,hospital_address,format=None):
        hospital = get_object_or_404(Hospital,name=hospital_name,address=hospital_address)

        if Patient.objects.filter(hospital=hospital).exists():
            return Response(
                {"details:cannot delete hospital as there are patient there"},
                status=status.HTTP_404_NOT_FOUND
            )
        hospital.delete()
        return Response({"details:Now can delete the hospital as there are no patient admitted"},
                        status=status.HTTP_204_NO_CONTENT)


class PatientView(APIView):
    def get(self,request):
        patient = Patient.objects.all().values('id','patient_name','contact_number','department','disease','patient_address','hospital')
        patient_list = list(patient)
        return JsonResponse(patient_list,safe=False)

class Patient_View_By_Number(APIView):    
    def get(self, request, contact_number):
            try:
                patient = Patient.objects.get(contact_number=contact_number)
                serializer = PatientSerializer(patient)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Patient.DoesNotExist:
                return Response({'error': 'No patient found with this contact number'}, status=status.HTTP_404_NOT_FOUND)

class PatientsByHospitalView(APIView):

    def get(self, request, hospital_name):
        try:
            hospital = Hospital.objects.get(name=hospital_name)
            patients = Patient.objects.filter(hospital=hospital).select_related('hospital')
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)


class PatientCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer =  PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PatientVisitView(APIView):
    def get(self,request):
        patientvisit = PatientVisit.objects.all().values('patient','hospital','hospital_visits','doctor_name','patient_status','medicine')
        patient_visit_list = list(patientvisit)
        return JsonResponse(patient_visit_list,safe=False)

class PatientVisitCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = PatientVisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PatientVisitNumberView(APIView):

    def get(self, request):
        contact_number = request.query_params.get('contact_number', None)
        if not contact_number:
            return Response({"error": "Contact number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(contact_number=contact_number)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        
        patient_visits = PatientVisit.objects.filter(patient=patient)
        serializer = PatientVisitSerializer(patient_visits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

           
class DischargePatientView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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