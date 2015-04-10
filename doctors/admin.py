from django.contrib import admin

from doctors.models import Doctor


class DoctorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Doctor, DoctorAdmin)
