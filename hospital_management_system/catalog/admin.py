from django.contrib import admin

from .models import Patient,Hospital,PatientStatus


admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(PatientStatus)
