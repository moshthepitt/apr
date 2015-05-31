from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from venues.views import VenueDatatableView, VenueAdd, VenueUpdate, VenueDelete, VenueView

urlpatterns = patterns('',
    url(r'^$', login_required(VenueDatatableView.as_view()), name='list'),
    url(r'^add/$', login_required(VenueAdd.as_view()), name='add'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(VenueUpdate.as_view()), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(VenueDelete.as_view()), name='delete'),
    url(r'^schedule/(?P<pk>\d+)/$', login_required(VenueView.as_view()), name='venue'),
)
