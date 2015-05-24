from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from apr.views import HomeView, DashboardView, CustomerRedirect

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
    url(r'^appointments/', include('appointments.urls', namespace='appointments')),

    url(r'^admin/', include(admin.site.urls)),

    # third party
    url(r'^select2/', include('django_select2.urls')),
    url(r'^accounts/', include('allauth.urls')),

    # utils
    url(r'^customer-redirector/$', CustomerRedirect.as_view(), name='customer_redirect'),

    # flat pages
    url(r'^page/', include('django.contrib.flatpages.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )
