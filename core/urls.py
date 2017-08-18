from django.conf.urls import url

from . import views

app_name = 'core'

urlpatterns = [
  url(r'^version/$', views.Version.version_info, name='version_info'),
  url(r'^country/(?P<country_id>[0-9]+)/state/(?P<state_id>[0-9]+)/$', views.StateView.state_element, name='state_element'),
  url(r'^country/(?P<country_id>[0-9]+)/state/$', views.StateView.state_collection, name='state_collection'),
  url(r'^country/(?P<country_id>[0-9]+)/$', views.CountryView.country_element, name='country_element'),
  url(r'^country/$', views.CountryView.country_collection, name='country_collection'),
  url(r'^forget_password/$', views.ForgetPasswordView.forget_password, name='forget_password'),
  url(r'^reset_password/$', views.ForgetPasswordView.reset_password, name='reset_password'),
]
