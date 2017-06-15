from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [
	url(r'account/(?P<id>[0-9]+)/nearest_partner/$', views.AccountView.nearest_partner, name='nearest_partner'),
    url(r'account/(?P<id>[0-9]+)/$', views.AccountView.account_element, name='account_element'),
    url(r'account/', views.AccountView.account_collection, name='account_collection'),
]
