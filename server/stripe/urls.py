from django.conf.urls import url

from . import views

app_name = 'stripe'

urlpatterns = [
    url(r'^customer/(?P<id>[0-9]+)/$', views.CustomerView.customer_element, name='customer_element'),
    url(r'^customer/', views.CustomerView.customer_collection, name='customer_collection'),
    url(r'^creditcard/(?P<id>[0-9]+)/$', views.CreditCardView.creditcard_element, name='creditcard_element'),
    url(r'^creditcard/', views.CreditCardView.creditcard_collection, name='creditcard_collection'),
    url(r'^bankaccount/(?P<id>[0-9]+)/$', views.BankAccountView.bankaccount_element, name='bankaccount_element'),
    url(r'^bankaccount/', views.BankAccountView.bankaccount_collection, name='bankaccount_collection'),
]
