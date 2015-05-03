from django.views.generic.detail import DetailView

from doctors.models import Doctor
from venues.models import Venue


class DoctorView(DetailView):
    model = Doctor
    template_name = "doctors/doctor_calendar.html"

    def get_context_data(self, **kwargs):
        context = super(DoctorView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.all()
        return context
