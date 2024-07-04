from django.contrib import admin
from django.urls import path, include,re_path
from hospital_app.views import PatientsByHospitalView,DischargePatientView,GetPatientStatusByDateView,DeleteHospital,PatientView,PatientCreate,Patient_View_By_Number,HospitalCreate,HospitalView,PatientVisitView,PatientVisitCreate,PatientVisitNumberView
from rest_framework import routers
from . import views


urlpatterns = [
    
    re_path('login', views.login),
    re_path('signup', views.signup),
    path('hospitals/<str:hospital_name>/patients/', PatientsByHospitalView.as_view(), name='patients-by-hospital'),
    path('hospital-create/',HospitalCreate.as_view(),name='hospitalcreate'),
    path('hospital-view/',HospitalView.as_view(),name='hospital-view'),
    path('discharge-patient/', DischargePatientView.as_view(), name='discharge-patient'),
    path('patient-status/', GetPatientStatusByDateView.as_view(), name='patient-status-by-date'),
    path('hospitals/delete/<str:hospital_name>/<str:hospital_address>/',DeleteHospital.as_view(),name='delete-hospital'),
    path('patient-view/',PatientView.as_view(),name='patientview'),
    path('patient-create/',PatientCreate.as_view(),name='patientcreate'),
    path('patient/<str:contact_number>/',Patient_View_By_Number.as_view(),name='patient_by_number'),
    path('patient-visit-view/',PatientVisitView.as_view(),name='patient-visit-view'),
    path('patient-visit-create/',PatientVisitCreate.as_view(),name='patientvisitcreate'),
    path('patient-visit-contact/',PatientVisitNumberView.as_view(),name='patient-visit-contact')
    
]

