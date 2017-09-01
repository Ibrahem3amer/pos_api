from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from pos import api_views

urlpatterns = [
    url(r'^receipts/$', api_views.receipts_list, name = 'api_receipts_list'),
    url(r'^receipts/(?P<receipt_id>[0-9]+)/$', api_views.receipt_instance, name = 'api_receipts_instance'),
]

urlpatterns = format_suffix_patterns(urlpatterns)