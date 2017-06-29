from django.conf.urls import url

from . import views

app_name = 'purchase'

urlpatterns = [
    url(r'(?P<id>[0-9]+)/$', views.PurchaseView.purchase_element, name='purchase_element'),
    url(r'^', views.PurchaseView.purchase_collection, name='purchase_collection'),
]
