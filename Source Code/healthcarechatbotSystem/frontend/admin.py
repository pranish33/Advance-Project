from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "HealthCare"
admin.site.site_title = "HealthCare"
admin.site.index_title = "HealthCare"


admin.site.register(Doctor)
admin.site.register(Contact)
admin.site.register(Patient)
admin.site.register(Appointment)