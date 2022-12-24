from django.conf.urls import url

from account.views import *

urlpatterns = [
      url(r'transaction/list/$', TransactionListview.as_view(), name="transaction_list")
]