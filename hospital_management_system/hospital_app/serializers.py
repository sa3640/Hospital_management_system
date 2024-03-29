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

class PatientSerializer(serializers.ModelSerializer):
    #id = serializers.UUIDField()
    #hospital_details = serializers.PrimaryKeyRelatedField(source="hospital",many=False,queryset=Hospital.objects.all())
    #hospital_name = HospitalSerializer(source='hospital',read_only=True)

    class Meta:
        model = Patient
        fields =(
                 'patient_name',
                 'contact_number',
                 'patient_address',
                 'department',
                 'disease')    


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
        
