from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'apr.views.home', name='home'),
    url(r'^appointments/', include('appointments.urls', namespace='appointments')),

    url(r'^admin/', include(admin.site.urls)),

    #third party
    url(r'^select2/', include('django_select2.urls')),
    url(r'^sc/', include('schedule.urls')), #to be removed
)
