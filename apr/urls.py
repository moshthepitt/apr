from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from apr.views import HomeView, DashboardView, CustomerRedirect, PDFView, PricingView
from apr.views import SupportView
from customers.views import NewCustomer

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^pricing/$', PricingView.as_view(), name='pricing'),
    url(r'^support/$', SupportView.as_view(), name='support'),
    url(r'^help/$', SupportView.as_view(template_name="core/help.html"), name='help'),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
    url(r'^pdf/$', login_required(PDFView.as_view()), name='pdf'),
    url(r'^new/$', login_required(NewCustomer.as_view()), name='new_customer'),
    url(r'^appointments/', include('appointments.urls', namespace='appointments')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^schedules/', include('venues.urls', namespace='venues')),

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
