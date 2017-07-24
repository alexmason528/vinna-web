from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [
    url(r'account/(?P<id>[0-9]+)/send_code/$', views.AccountView.send_code, name='send_code'),
    url(r'account/(?P<id>[0-9]+)/verify_phone/$', views.AccountView.verify_phone, name='verify_phone'),
    url(r'account/(?P<id>[0-9]+)/verify_email/$', views.AccountView.verify_email, name='verify_email'),
    url(r'account/(?P<id>[0-9]+)/purchase_info/$', views.AccountView.purchase_info, name='purchase_info'),
    url(r'account/(?P<id>[0-9]+)/nearest_partner/$', views.AccountView.nearest_partner, name='nearest_partner'),
    url(r'account/(?P<id>[0-9]+)/$', views.AccountView.account_element, name='account_element'),
    url(r'account/', views.AccountView.account_collection, name='account_collection'),
]
