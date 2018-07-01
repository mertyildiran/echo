from django.conf.urls import url
from core import views


urlpatterns = [
    url(r'^echos/$', views.echo_list),
    url(r'^echos/(?P<pk>[0-9]+)/$', views.echo_detail),
]
