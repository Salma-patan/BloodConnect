from django.contrib import admin
from .models import Registration,login,Contact,donateblood,patientrequest,donorreg,CampRegistration

admin.site.register(Registration)
admin.site.register(login)
admin.site.register(Contact)
admin.site.register(donateblood)
admin.site.register(patientrequest)
admin.site.register(donorreg)
admin.site.register(CampRegistration)