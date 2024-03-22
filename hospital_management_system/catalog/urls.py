from django.contrib import admin
from django.urls import path, include,re_path
from catalog.views import PatientVisitViewSet,HospitalViewSet,PatientViewSet
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'hospitals',HospitalViewSet)
router.register(r'patientvisit',PatientVisitViewSet)
router.register(r'patient',PatientViewSet)
urlpatterns = [
    path('',include(router.urls)),
    re_path('login', views.login),
    re_path('signup', views.signup)
    
    
]

