from django.contrib import admin
from django.urls import path, include
from catalog.views import PatientVisitViewSet,HospitalViewSet,PatientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'hospitals',HospitalViewSet)
router.register(r'patientvisit',PatientVisitViewSet)
router.register(r'patient',PatientViewSet)
urlpatterns = [
    path('',include(router.urls))
]

