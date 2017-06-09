from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [
	url(r'account/(?P<id>[0-9]+)/nearest_partner/$', views.AccountView.nearest_partner, name='nearest_partner'),
    url(r'account/(?P<id>[0-9]+)/$', views.AccountView.account_element, name='account_element'),
    url(r'account/', views.AccountView.account_collection, name='account_collection'),
    url(r'role/(?P<id>[0-9]+)/$', views.RoleView.role_element, name='role_element'),
    url(r'role/', views.RoleView.role_collection, name='role_collection'),
    
    #url(r'^$', views.index, name='index'),


    #url(r'^$', views.login, name='login'),
    #url(r'^register/step2/$', views.register_step_2, name='register_step_2'),
    #url(r'^login/$', views.login, name='login'),
    #url(r'^register/$', views.login, name='login'),
]
