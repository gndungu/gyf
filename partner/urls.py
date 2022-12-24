from django.conf.urls import url
from partner.views import *

urlpatterns = [
    url(r'staff/list/$', PartnerStaffListView.as_view(), name='staff_list'),
    url(r'staff/list/(?P<pk>[\w]+)/$', PartnerStaffListView.as_view(), name='staff_list'),
    url(r'staff/create/$', PartnerStaffCreateView.as_view(), name='staff_create'),
    url(r'staff/create/(?P<pk>[\w]+)/$', PartnerStaffCreateView.as_view(), name='staff_create'),
    url(r'staff/(?P<code>[\w]+)/(?P<pk>[\w]+)/$', PartnerStaffUpdateView.as_view(), name='staff_edit'),
    
    url(r'list/$', PartnerListView.as_view(), name='list'),
    url(r'create/$', PartnerCreateView.as_view(), name='create'),
    url(r'partner/(?P<pk>[\w]+)/$', PartnerDetailView.as_view(), name='detail'),
    url(r'(?P<pk>[\w]+)/$', PartnerUpdateView.as_view(), name='edit')
]