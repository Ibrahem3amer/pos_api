from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from pos import api_views

urlpatterns = [
    url(r'^receipts/average/(?P<receipt_id>[0-9]+)/$', api_views.receipt_avg, name = 'api_receipt_average'),
    url(r'^receipts/pay/(?P<receipt_id>[0-9]+)/$', api_views.pay_receipt, name = 'api_pay_receipt'),
    url(r'^receipts/$', api_views.receipts_list, name = 'api_receipts_list'),
    url(r'^receipts/(?P<receipt_id>[0-9]+)/$', api_views.receipt_instance, name = 'api_receipts_instance'),
    url(r'^items/$', api_views.items_list, name = 'api_items_list'),
    url(r'^items/receipt/(?P<receipt_id>[0-9]+)/$', api_views.items_list, name = 'api_receipt_items_list'),
    url(r'^items/(?P<item_id>[0-9]+)/$', api_views.item_instance, name = 'api_item_instance'),
]

urlpatterns = format_suffix_patterns(urlpatterns)