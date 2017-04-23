from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<member_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
]