from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^detail/$', views.detail, name='detail'),
    #url(r'^register/$', views.register, name='register'),
    #url(r'^.*/$', views.direct, name='direct'),
]
