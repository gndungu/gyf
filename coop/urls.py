from django.conf.urls import url

from coop.views.cooperative import *
from coop.views.member import *
from coop.views.collection import *
from coop.views.order import *
from coop.views.farmer_group import *
from coop.views.agent import *
from coop.views.finance import *

urlpatterns = [

     url(r'financial/list/$', FinancialInstitutionListView.as_view(), name='finance_list'),
     url(r'financial/create/$', FinancialInstitutionCreateView.as_view(), name='finance_create'),
     url(r'financial/edit/(?P<pk>[\w]+)/$', FinancialInstitutionUpateView.as_view(), name='finance_edit'),


     url(r'offtaker/list/$', OffTakerListView.as_view(), name='offtaker_list'),
     url(r'offtaker/create/$', OffTakerCreateView.as_view(), name='offtaker_create'),
     url(r'offtaker/edit/(?P<pk>[\w]+)/$', OffTakerUpateView.as_view(), name='offtaker_edit'),

     url(r'agent/list/$', AgentListView.as_view(), name='agent_list'),
     url(r'agent/create/$', AgentCreateFormView.as_view(), name='agent_create'),
     url(r'agent/edit/(?P<pk>[\w]+)/$', AgentUpdateFormView.as_view(), name='agent_edit'),
     url(r'agent/upload/$', AgentUploadView.as_view(), name='agent_upload'),

     url(r'order/status/(?P<pk>[\w]+)/(?P<status>[\w]+)$', MemberOrderStatusView.as_view(), name='order_status'),
     url(r'order/item/list/$', MemberOrderItemListView.as_view(), name='order_item_list'),
     url(r'order/item/status/(?P<pk>[\w]+)/(?P<status>[\w]+)$', OrderItemStatusView.as_view(), name='item_status'),

     url(r'order/delete/(?P<pk>[\w]+)/$', MemberOrderDeleteView.as_view(), name='order_delete'),
     url(r'order/detail/(?P<pk>[\w]+)/$', MemberOrderDetailView.as_view(), name='order_detail'),
     url(r'order/create/(?P<pk>[\w]+)/$', MemberOrderCreateView.as_view(), name='order_update'),
     url(r'order/create/$', MemberOrderCreateView.as_view(), name='order_create'),
     url(r'order/list/$', MemberOrderListView.as_view(), name='order_list'),
     url(r'order/upload/$', OrderUploadView.as_view(), name='order_upload'),
    
     url(r'collection/download/$', CollectionDownload.as_view(), name='collection_download'),
     url(r'collection/create/$', CollectionCreateView.as_view(), name='collection_update'),
     url(r'collection/create/$', CollectionCreateView.as_view(), name='collection_create'),
     url(r'collection/list/$', CollectionListView.as_view(), name='collection_list'),
     
     url(r'member/shares/$', MemberSharesView.as_view(), name='member_shares'),
     
     url(r'member/shares/list/(?P<member>[\w]+)/$', MemberSharesListView.as_view(), name='member_shares_list'),
     url(r'member/shares/list/$', MemberSharesListView.as_view(), name='member_shares_list'),
     url(r'member/shares/create/$', MemberSharesCreateView.as_view(), name='member_shares_create'),
     url(r'member/shares/(?P<pk>[\w]+)/$', MemberSharesUpdateView.as_view(), name='member_shares_update'),
     
     url(r'member/subscription/list/$', MemberSubscriptionListView.as_view(), name='member_subscription_list'),
     url(r'member/subscription/create/$', MemberSubscriptionCreateView.as_view(), name='member_subscription_create'),
     url(r'member/subscription/(?P<pk>[\w]+)/$', MemberSubscriptionUpdateView.as_view(), name='member_subscription_update'),
     
     url(r'share/price/list/$', CooperativeSharePriceListView.as_view(), name='share_price_list'),
     url(r'share/price/create/$', CooperativeSharePriceCreateView.as_view(), name='share_price_create'),
     url(r'share/price/(?P<pk>[\w]+)/$', CooperativeSharePriceUpdateView.as_view(), name='share_price_update'),

     url(r'fg/delete/(?P<pk>[\w]+)/$', FarmerGroupDeleteView.as_view(), name='fg_delete'),
     url(r'fg/update/(?P<pk>[\w]+)/$', FarmerGroupUpdateView.as_view(), name='fg_update'),
     url(r'fg/detail/(?P<pk>[\w]+)/$', FarmerGroupDetailView.as_view(), name='fg_detail'),
     url(r'fg/upload/$', FarmerGroupUploadView.as_view(), name='fg_upload'),
     url(r'fg/create/$', FarmerGroupCreateView.as_view(), name='fg_create'),
     url(r'fg/list/$', FarmerGroupListView.as_view(), name='fg_list'),
     
     
     url(r'ajax/village/$', load_villages, name='ajax_load_village'),
     url(r'ajax/member/$', load_coop_members, name='ajax_load_members'),
     
     url(r'communication/send/$', SendCommunicationView.as_view(), name='communication_send'),
     
     url(r'contribution/list/$', CooperativeContributionListView.as_view(), name='contribution_list'),
     url(r'contribution/create/$', CooperativeContributionCreateView.as_view(), name='contribution_create'),
     url(r'contribution/(?P<pk>[\w]+)/$', CooperativeContributionUpdateView.as_view(), name='contribution_update'),
     url(r'share/list/$', CooperativeShareTransactionListView.as_view(), name='share_list'),
     url(r'share/create/$', CooperativeShareTransactionCreateView.as_view(), name='share_create'),
     url(r'share/(?P<pk>[\w]+)/$', CooperativeShareTransactionUpdateView.as_view(), name='share_update'),
     url(r'member/delete/(?P<pk>[\w]+)/$', MemberDeleteView.as_view(), name='member_delete'),
     url(r'member/detail/(?P<pk>[\w]+)/$', CooperativeMemberDetailView.as_view(), name='member_detail'),
     url(r'member/qrcode/(?P<pk>[\w]+)/$', ImageQRCodeDownloadView.as_view(), name='member_qrcode'),
     url(r'member/download/$', DownloadExcelMemberView.as_view(), name='member_download'),
     url(r'member/upload/$', MemberUploadExcel.as_view(), name='member_upload'),
     url(r'member/list/$', CooperativeMemberListView.as_view(), name='member_list'),
     url(r'member/create/$', MemberCreateView.as_view(), name='member_create'),
     url(r'member/map/$', MembersMapView.as_view(), name='member_map'),
     url(r'member/(?P<pk>[\w]+)/$', MemberUpdateView.as_view(), name='member_update'),
     url(r'delete/(?P<pk>[\w]+)/$', CooperativeDeleteView.as_view(), name='delete'),
     url(r'upload/$', CooperativeUploadView.as_view(), name='upload'),
     url(r'create/$', CooperativeCreateView.as_view(), name='create'),
     url(r'list/$', CooperativeListView.as_view(), name='list'),
     url(r'ajax/load-farmer/', get_farmer_map, name='ajax_load_farmer_map'),
     url(r'(?P<pk>[\w]+)/$', CooperativeUpdateView.as_view(), name='edit'),
     
    ]