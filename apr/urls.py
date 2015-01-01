from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apr.views.home', name='home'),
    url(r'^appointments/', include('appointments.urls', namespace='appointments')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sc/', include('schedule.urls')),

)
