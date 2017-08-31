from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from pos import api_views

urlpatterns = [
    url(r'^receipts/$', api_views.topics_list, name = 'api_topics_list'),
    url(r'^topics/(?P<topic_id>[0-9]+)/materials/$', api_views.materials_list, name = 'api_materials_list'),
    url(r'^topics/(?P<topic_id>[0-9]+)/exams/$', api_views.exams_list, name = 'api_exams_list'),
    url(r'^topics/(?P<pk>[0-9]+)$', api_views.topic_instance, name = 'api_topic'),
    url(r'^topics/faculty/(?P<fac_id>[0-9]+)$', api_views.topic_faculty, name = 'api_faculty_topics'),
    url(r'^topics/query_table/$', api_views.query_dep_table, name = 'api_query_table'),
    url(r'^users/(?P<user_id>[0-9]+)/main_table/$', main_table, name = 'api_main_table'),
    url(r'^users/(?P<user_id>[0-9]+)/table/$', user_table, name = 'api_user_table'),
]

urlpatterns = format_suffix_patterns(urlpatterns)