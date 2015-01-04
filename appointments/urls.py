from django.conf.urls import patterns, url

from .ajax import event_feed
from .views import AddEventView

urlpatterns = patterns('',
    url(r'^feed/', event_feed, name='event_feed'),
    url(r'^add/', AddEventView.as_view(), name='add'),
)
