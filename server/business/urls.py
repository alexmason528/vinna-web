from django.conf.urls import url

from . import views

app_name = 'business'

urlpatterns = [
	url(r'^(?P<id>[0-9]+)/billing_info/(?P<binfo_id>[0-9]+)/$', views.BusinessBillingInfoView.business_billing_info_element, name='business_billing_info_element'),
    url(r'^(?P<id>[0-9]+)/billing_info/$', views.BusinessBillingInfoView.business_billing_info_collection, name='business_billing_info_collection'),
    url(r'^(?P<id>[0-9]+)/$', views.BusinessView.business_element, name='business_element'),
    url(r'^', views.BusinessView.business_collection, name='business_collection'),
]
