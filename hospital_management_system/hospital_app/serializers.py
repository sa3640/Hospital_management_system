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
        # depth = 1
        fields = (
                  'name',
                  'address',
                  'staffs_num',
                  'num_of_beds'
                  )

class HospitalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('name',
                  'address')

class PatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Patient
        
        fields = '__all__'    


class PatientVisitSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = PatientVisit
    
        fields= '__all__' 
        
