from django.conf.urls import patterns, url

from .ajax import event_feed, process_add_user_form, process_select_user_form
from .views import AddEventView

urlpatterns = patterns('',
    #ajax
    url(r'^feed/', event_feed, name='event_feed'),
    url(r'^add-user-form/', process_add_user_form, name='process_add_user_form'),
    url(r'^select-user-form/', process_select_user_form, name='process_select_user_form'),
    #regular
    url(r'^add/', AddEventView.as_view(), name='add'),
)
