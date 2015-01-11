from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from appointments.ajax import event_feed, process_add_client_form, process_select_client_form, process_add_event_form
from appointments.views import AddEventView, AppointmentView

urlpatterns = patterns('',
    #ajax
    url(r'^feed/', event_feed, name='event_feed'),
    url(r'^add-client-form/', login_required(process_add_client_form), name='process_add_client_form'),
    url(r'^select-client-form/', login_required(process_select_client_form), name='process_select_client_form'),
    url(r'^add-event-form/', login_required(process_add_event_form), name='process_add_event_form'),
    #regular
    url(r'^add/', login_required(AddEventView.as_view()), name='add'),
    url(r'^view/(?P<pk>\d+)/$', AppointmentView.as_view(), name='appointment'),
)
