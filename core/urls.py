from django.conf.urls import url
from core import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^echos/$', views.EchoList.as_view()),
    url(r'^echo/(?P<pk>[0-9]+)/$', views.EchoDetail.as_view()),
    url(r'^staff_echos/$', views.StaffOnlyEchoList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^staff_users/$', views.StaffOnlyUserList.as_view()),
    url(r'^register/$', views.Register.as_view()),
    url(r'^login/$', views.Login.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
