from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [
    #url(r'^details/$', views.account_list, name='list'),
    # url(r'^(?P<id>[0-9]+)/account_role/(?P<pinfo_id>[0-9]+)/$', views.MemberPaymentInfoView.member_payment_info_element, name='member_payment_info_element'),
    # url(r'^(?P<id>[0-9]+)/account_role/$', views.MemberPaymentInfoView.member_payment_info_collection, name='member_payment_info_collection'),
    url(r'^(?P<id>[0-9]+)/$', views.AccountView.account_element, name='account_element'),
    url(r'^', views.AccountView.account_collection, name='account_collection'),
    
    #url(r'^$', views.index, name='index'),


    #url(r'^$', views.login, name='login'),
    #url(r'^register/step2/$', views.register_step_2, name='register_step_2'),
    #url(r'^login/$', views.login, name='login'),
    #url(r'^register/$', views.login, name='login'),
]
