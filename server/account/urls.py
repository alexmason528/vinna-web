from django.conf.urls import url

from . import views
from server.purchase import views as purchase_views

app_name = 'account'

urlpatterns = [
    url(r'account/find_phone', views.AccountView.find_phone, name='find_phone'),
    url(r'account/find_email', views.AccountView.find_email, name='find_email'),
    url(r'account/(?P<id>[0-9]+)/send_phone_code', views.AccountView.send_phone_code, name='send_phone_code'),
    url(r'account/(?P<id>[0-9]+)/send_email_code', views.AccountView.send_email_code, name='send_email_code'),
    url(r'account/(?P<id>[0-9]+)/verify_phone', views.AccountView.verify_phone, name='verify_phone'),
    url(r'account/(?P<id>[0-9]+)/verify_email', views.AccountView.verify_email, name='verify_email'),
    url(r'account/(?P<id>[0-9]+)/update_phone', views.AccountView.update_phone, name='update_phone'),
    url(r'account/(?P<id>[0-9]+)/update_email', views.AccountView.update_email, name='update_email'),
    url(r'account/(?P<id>[0-9]+)/purchase_info', views.AccountView.purchase_info, name='purchase_info'),
    url(r'account/(?P<id>[0-9]+)/purchase_summary', views.AccountView.purchase_info, name='purchase_summary'),
    url(r'account/(?P<id>[0-9]+)/nearest_partner', views.AccountView.nearest_partner, name='nearest_partner'),
    url(r'account/(?P<id>[0-9]+)/purchase', views.AccountView.purchase_collection, name='purchase'),
    url(r'account/(?P<id>[0-9]+)', views.AccountView.account_element, name='account_element'),
    url(r'account', views.AccountView.account_collection, name='account_collection'),
]
