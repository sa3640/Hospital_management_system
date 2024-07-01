from django.contrib import admin
from django.urls import path
from .views import Login,Signup,Patient_Status_Patient_name,PatientVisitUpdate,PatientVisitStatus,PatientCreate,PatientInfo


urlpatterns = [
    path('patientstatus',Patient_Status_Patient_name.as_view(),name='Patient_status'),
    path('login', Login.as_view(), name='login'),
    path('signup',Signup.as_view(),name='signup'),
    path('update-patient-visit/<str:contact_number>', PatientVisitUpdate.as_view(), name='update-patient-visit'),
    path('patientvisit', PatientVisitStatus.as_view(), name='patient-visit-status'),
    path('createpatient',PatientCreate.as_view(),name="patient_create"),
    path('patient',PatientInfo.as_view(),name="get_patient")
    ]

