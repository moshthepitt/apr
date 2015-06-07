from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from customers.views import EditCustomer, EditCustomerScript, EditCustomerSettings

urlpatterns = patterns('',
    url(r'^edit/$', login_required(EditCustomer.as_view()), name='edit'),
    url(r'^script/$', login_required(EditCustomerScript.as_view()), name='script'),
    url(r'^settings/$', login_required(EditCustomerSettings.as_view()), name='settings'),
)
