from rest_framework import serializers
from .models import Patient,Hospital,PatientStatus

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id',
                  'name',
                  'address'
                  )
        
class PatientSerializer(serializers.ModelSerializer):
    #id = serializers.UUIDField()
    hospital_details = serializers.PrimaryKeyRelatedField(source="hospital",many=False,queryset=Hospital.objects.all())
    #hospital_name = HospitalSerializer(source='hospital',read_only=True)

    class Meta:
        model = Patient
        fields =('id',
                 'patient_name',
                 'hospital',
                 'hospital_details',
                 'doctor_name',
                 'department',
                 'disease')    


class PatientStatusSerializer(serializers.HyperlinkedModelSerializer):
    #patient = PatientSerializer()
    patient_details = serializers.PrimaryKeyRelatedField(source="patient",many=False,queryset=Patient.objects.all())

    class Meta:
        model = PatientStatus
        depth = 1
        fields=('patient',
                'patient_details',
                'primary_checkup',
                'consultation',
                'admitted',
                'discharged',
                'referred')          