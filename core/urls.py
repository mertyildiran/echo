from django.conf.urls import url
from core import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^echos/$', views.echo_list),
    url(r'^echos/(?P<pk>[0-9]+)/$', views.echo_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
