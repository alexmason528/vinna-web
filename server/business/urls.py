from django.conf.urls import url

from . import views
from server.purchase import views as purchase_views

app_name = 'business'

urlpatterns = [
  url(r'^(?P<business_id>[0-9]+)/purchases', purchase_views.PurchaseView.business_purchase_collection, name='business_purchases'),
  url(r'^(?P<id>[0-9]+)/cashier/(?P<cashier_id>[0-9]+)/purchase_summary', views.BusinessCashierView.business_cashier_purchase_summary, name='business_cashier_purchase_summary'),
	url(r'^(?P<id>[0-9]+)/cashier/(?P<cashier_id>[0-9]+)', views.BusinessCashierView.business_cashier_element, name='business_cashier_element'),
	url(r'^(?P<id>[0-9]+)/cashier', views.BusinessCashierView.business_cashier_collection, name='business_cashier_collection'),
  url(r'^(?P<id>[0-9]+)/purchase_summary', views.BusinessPurchaseView.business_purchase_summary, name='business_purchase_summary'),
	url(r'^(?P<id>[0-9]+)/purchase/(?P<purchase_id>[0-9]+)', views.BusinessPurchaseView.business_purchase_element, name='business_purchase_element'),
	url(r'^(?P<id>[0-9]+)/purchase', views.BusinessPurchaseView.business_purchase_collection, name='business_purchase_collection'),
	url(r'^(?P<id>[0-9]+)/billing_info/(?P<binfo_id>[0-9]+)', views.BusinessBillingInfoView.business_billing_info_element, name='business_billing_info_element'),
  url(r'^(?P<id>[0-9]+)/billing_info', views.BusinessBillingInfoView.business_billing_info_collection, name='business_billing_info_collection'),
  url(r'^(?P<id>[0-9]+)', views.BusinessView.business_element, name='business_element'),
  url(r'^', views.BusinessView.business_collection, name='business_collection'),
]
