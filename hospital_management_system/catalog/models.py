
import uuid
from django.db import models





# Create your models here.
class Hospital(models.Model):
    register_id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Registration id for hospitals')
    hosp_name = models.CharField(max_length=200, unique = True) 
    
    staff_number =  models.IntegerField()
    address = models.CharField(max_length=200, unique = True)
    numb_beds = models.IntegerField()

    def __str__(self):
        """String for representing the Model object."""
        return self.hosp_name
    

class Patient(models.Model):
    patient_id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='patients id')
    patient_name =  models.CharField(max_length=200,unique=True)
    
    register_id = models.ForeignKey('Hospital', on_delete = models.RESTRICT)
    doctor_name = models.CharField(max_length=200)
    dept_name = models.CharField(max_length=200,default="Surgery Department")
    patient_disease = models.CharField(max_length=200)
    primary_check = models.DateTimeField()
    consultation = models.DateTimeField()
    admitted = models.DateTimeField(null=True)
    referred = models.BooleanField()
    discharged = models.DateTimeField(null=True)

    def __str__(self):
        return self.patient_name
