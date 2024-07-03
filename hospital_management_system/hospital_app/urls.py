from django.contrib import admin
from django.urls import path, include,re_path
from hospital_app.views import PatientVisitViewSet,HospitalViewSet,PatientViewSet,PatientsByHospitalView,DischargePatientView,GetPatientStatusByDateView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'hospitals',HospitalViewSet)
router.register(r'patientvisit',PatientVisitViewSet)
router.register(r'patient',PatientViewSet)
urlpatterns = [
    path('',include(router.urls)),
    re_path('login', views.login),
    re_path('signup', views.signup),
    path('hospitals/<str:hospital_name>/patients/', PatientsByHospitalView.as_view(), name='patients-by-hospital'),
    path('discharge-patient/', DischargePatientView.as_view(), name='discharge-patient'),
    path('patient-status/', GetPatientStatusByDateView.as_view(), name='patient-status-by-date'),
    
]

