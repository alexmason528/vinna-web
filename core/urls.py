from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


from . import views

app_name = 'core'

urlpatterns = [
    url(r'^country/(?P<countryid>[0-9]+)/$', views.CountryView.country_element, name='country_element'),
    url(r'^country/', views.CountryView.country_collection, name='country_collection'),
    url(r'^state/(?P<stateid>[0-9]+)/$', views.StateView.state_element, name='state_element'),
    url(r'^state/', views.StateView.state_collection, name='state_collection'),
    url(r'^language/(?P<languageid>[0-9]+)/$', views.LanguageView.language_element, name='language_element'),
    url(r'^language/', views.LanguageView.language_collection, name='language_collection'),
]
