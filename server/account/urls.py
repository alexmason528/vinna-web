from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


from . import views

app_name = 'accounts_api'

urlpatterns = [
    #url(r'^details/$', views.account_list, name='list'),
    url(r'^details/(?P<userid>[0-9]+)$', views.AccountView.account_detail, name='details'),
    url(r'^obtain_auth_token/$', obtain_jwt_token),
    url(r'^refresh_auth_token/$', refresh_jwt_token),
    url(r'^verify_auth_token/', verify_jwt_token),
    
    #url(r'^$', views.index, name='index'),


    #url(r'^$', views.login, name='login'),
    #url(r'^register/step2/$', views.register_step_2, name='register_step_2'),
    #url(r'^login/$', views.login, name='login'),
    #url(r'^register/$', views.login, name='login'),
]
