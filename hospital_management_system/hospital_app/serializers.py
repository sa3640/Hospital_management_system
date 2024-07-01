from rest_framework import serializers
from .models import Patient,Hospital,PatientVisit
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
     class Meta(object):
         model = User
         fields = [ 'id' ,'username' , 'password' , 'email']


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = (
                  'name',
                  'address',
                  'Staffs_num',
                  'num_of_beds'
                  )

class HospitalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('name',
                  'address')

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_name', 'contact_number', 'department', 'disease', 'patient_address']

class PatientVisitSerializer(serializers.ModelSerializer):
    #patient = PatientSerializer()
    patient= serializers.ReadOnlyField(source='patient.patient_name')
    hospital = HospitalNameSerializer()
    


    class Meta:
        model = PatientVisit
        depth = 1
        fields=('patient',
                'hospital',
                'hospital_visits',
                'doctor_name',
                'patient_status',
                'medicine'
                )          
        
class PatientVisitStatusSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.patient_name')
    
    class Meta:
        model = PatientVisit
        fields = ['patient_name', 'patient_status']    


class PatientVisitUpdateSerializer(serializers.ModelSerializer):
    patient_contact_number = serializers.ReadOnlyField(source="patient.contact_number")
    class Meta:
        model = PatientVisit
        fields = ['patient_contact_number','patient_status', 'medicine']


class PatientVisitDateSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source="patient.patient_name") 
    hospital_name = serializers.ReadOnlyField(source='hospital.name')
    class Meta:
        model = PatientVisit
        fields = ['patient_name','hospital_name','hospital_visits', 'patient_status']        