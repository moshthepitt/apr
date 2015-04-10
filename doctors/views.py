from django.views.generic.detail import DetailView

from doctors.models import Doctor


class DoctorView(DetailView):
    model = Doctor
    template_name = "doctors/doctor_calendar.html"
