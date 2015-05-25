from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from appointments.ajax import event_feed, venue_event_feed, doctor_event_feed, printable_event_feed
from appointments.ajax import process_add_client_form, process_select_client_form, process_add_event_form
from appointments.views import AddEventView, AppointmentView, AppointmentListView, AppointmentDelete
from appointments.views import AppointmentEdit, AppointmentDatatableView
from venues.views import VenueView
from doctors.views import DoctorView


urlpatterns = patterns('',
    # ajax
    url(r'^feed/doctor/(?P<pk>\d+)/$', doctor_event_feed, name='doctor_event_feed'),
    url(r'^feed/venue/(?P<pk>\d+)/$', venue_event_feed, name='venue_event_feed'),
    url(r'^all-feed/$', event_feed, name='event_feed'),
    url(r'^printable-feed/$', printable_event_feed, name='printable_event_feed'),
    url(r'^add-client-form/$', login_required(process_add_client_form), name='process_add_client_form'),
    url(r'^select-client-form/$', login_required(process_select_client_form), name='process_select_client_form'),
    url(r'^add-event-form/$', login_required(process_add_event_form), name='process_add_event_form'),
    # regular
    url(r'^add/', login_required(AddEventView.as_view()), name='add'),
    url(r'^appointments/(?P<app_label>[\w-]+)/(?P<model_name>[\w-]+)/(?P<pk>\d+)/$', login_required(AppointmentListView.as_view()), name='appointments_filter'),
    # url(r'^appointments/$', login_required(AppointmentListView.as_view()), name='appointments'),
    url(r'^appointments/$', login_required(AppointmentDatatableView.as_view()), name='appointments'),
    url(r'^view/(?P<pk>\d+)/$', login_required(AppointmentView.as_view()), name='appointment'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(AppointmentEdit.as_view()), name='appointment_edit'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(AppointmentDelete.as_view()), name='appointment_delete'),
    url(r'^venue/(?P<pk>\d+)/$', login_required(VenueView.as_view()), name='venue'),
    url(r'^doctor/(?P<pk>\d+)/$', login_required(DoctorView.as_view()), name='doctor'),
)
