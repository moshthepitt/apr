from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from apr.views import home

urlpatterns = patterns('',
    url(r'^$', login_required(home), name='home'),
    url(r'^appointments/', include('appointments.urls', namespace='appointments')),

    url(r'^admin/', include(admin.site.urls)),

    # third party
    url(r'^select2/', include('django_select2.urls')),
    url(r'^accounts/', include('allauth.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )
