from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from users.views import ClientDatatableView, ClientAdd, ClientUpdate, ClientDelete, ClientView

urlpatterns = patterns('',
    url(r'^$', login_required(ClientDatatableView.as_view()), name='list'),
    url(r'^add/$', login_required(ClientAdd.as_view()), name='add'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(ClientUpdate.as_view()), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(ClientDelete.as_view()), name='delete'),
    url(r'^client/(?P<pk>\d+)/$', login_required(ClientView.as_view()), name='client'),
)
