from django.conf.urls import url

from . import views

app_name = 'member'

urlpatterns = [
	url(r'^(?P<id>[0-9]+)/pinfo/(?P<pinfo_id>[0-9]+)/$', views.MemberPaymentInfoView.member_payment_info_element, name='member_payment_info_element'),
	url(r'^(?P<id>[0-9]+)/pinfo/$', views.MemberPaymentInfoView.member_payment_info_collection, name='member_payment_info_collection'),
    url(r'^(?P<id>[0-9]+)/$', views.MemberView.member_element, name='member_element'),
    url(r'^', views.MemberView.member_collection, name='member_collection'),
]
