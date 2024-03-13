import uuid
from django.db import models

class Hospital(models.Model):
    id = models.UUIDField(primary_key = True,default=uuid.uuid4,unique=True,editable=False)
    name = models.CharField(max_length=200,default='')
    address = models.TextField(max_length=1000,default='')

    def __str__(self):
        return str(self.name)
    
class Patient(models.Model):
    id = models.UUIDField(primary_key = True,default=uuid.uuid4,unique=True,editable=False)
    patient_name = models.CharField(max_length=200,default='')
    hospital =models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name="patients")
    doctor_name = models.CharField(max_length=200,default='')
    department =  models.CharField(max_length=200,default='')
    disease = models.CharField(max_length=200,default='')

    def __str__(self):
        return str(self.id)
    
class PatientStatus(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="patientstatus")
    primary_checkup =    models.TextField(max_length=1000,default='')
    consultation = models.TextField(max_length=1000,default='')
    admitted = models.BooleanField(default=False)
    discharged = models.BooleanField(default=False)
    referred = models.BooleanField(default=False)

    def __str__(self):
        return str(self.patient)





