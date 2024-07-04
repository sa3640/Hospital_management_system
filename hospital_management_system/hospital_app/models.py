import uuid
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token as DefaultToken
from django.core.validators import RegexValidator
from datetime import datetime

class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200, default='',unique=True,blank=False, null=False)
    address = models.TextField(max_length=1000, default='',unique=True,null=False)
    staffs_num = models.IntegerField()
    num_of_beds = models.IntegerField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    patient_name = models.CharField(max_length=200, default='',blank=False, null=False)
    contact_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits',
                code='invalid_phone_number'
            ),
        ],
        blank=False, null=False
    )
    department = models.CharField(max_length=200, default='',blank=False, null=False)
    disease = models.CharField(max_length=200, default='',blank=False, null=False)
    patient_address = models.CharField(max_length=200, default='',blank=False, null=False)
    hospital = models.ForeignKey(Hospital, related_name='patients', on_delete=models.CASCADE)

    def __str__(self):
        return self.patient_name

class PatientVisit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="patientname")
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name="hospitalname")
    hospital_visits = models.DateField(blank=False,null=False)
    doctor_name = models.CharField(max_length=200, default='',blank=False, null=False)
    patient_status = models.CharField(max_length=200, default='', blank=False,null=False)
    medicine = models.CharField(max_length=100, default='', blank=False)
    timestamp = models.DateTimeField(default=datetime.now, editable=True)

    def __str__(self):
        return str(self.patient)
