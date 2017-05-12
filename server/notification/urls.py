from django.conf.urls import url

from . import views

app_name = 'notification'

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', views.NotificationView.notification_element, name='notification_element'),
    url(r'^', views.NotificationView.notification_collection, name='notification_collection'),
]
