from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


from . import views

app_name = 'member'

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', views.MemberView.member_element, name='member_element'),
    url(r'^', views.MemberView.member_collection, name='member_collection'),
]
