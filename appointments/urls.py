from django.conf.urls import patterns, url

from .ajax import event_feed

urlpatterns = patterns('',
    url(r'^feed/', event_feed, name='event_feed'),
)
