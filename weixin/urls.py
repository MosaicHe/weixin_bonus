from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_openid', views.get_openid, name='get_openid'),
    url(r'^get_userinfo', views.get_userinfo, name='get_userinfo'),
    url(r'^index', views.index, name='index'),
    url(r'^token', views.token, name='token'),
]
