from django.conf.urls import url

from . import views

app_name = 'business'

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/billinginfo/$', views.BusinessBillingInfoView.business_billing_info, name='business_billing_info'),
    url(r'^(?P<id>[0-9]+)/$', views.BusinessView.business_element, name='business_element'),
    url(r'^', views.BusinessView.business_collection, name='business_collection'),
]
