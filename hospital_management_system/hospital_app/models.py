import uuid
from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    models.UUIDField(primary_key = True,default=uuid.uuid4,unique=True,editable=False)
    name = models.CharField(max_length=200,default='')
    address = models.TextField(max_length=1000,default='')
    Staffs_num = models.IntegerField()
    num_of_beds = models.IntegerField(unique=True)


    def __str__(self):
        return str(self.name)
    
class Patient(models.Model):
    models.UUIDField(primary_key = True,default=uuid.uuid4,unique=True,editable=False)
    patient_name = models.CharField(max_length=200,default='')
    contact_number = models.CharField(max_length=200,default='',null=False,unique=True)
    department =  models.CharField(max_length=200,default='')
    disease = models.CharField(max_length=200,default='')
    patient_address = models.CharField(max_length=200,default='')
    

    def __str__(self):
        return str(self.patient_name)
    
class PatientVisit(models.Model):
    id = models.UUIDField(primary_key = True,default=uuid.uuid4,unique=True,editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="patientname")
    hospital =models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name="hospitalname")
    hospital_visits = models.DateField(blank=False)
    doctor_name = models.CharField(max_length=200,default='')
    patient_status = models.CharField(max_length=200,default='',blank=False,)
    medicine = models.CharField(max_length=100,default='',blank=False,)
   
    def __str__(self):
        return str(self.patient)




