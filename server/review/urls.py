from django.conf.urls import url

from . import views

app_name = 'review'

urlpatterns = [
  url(r'^(?P<id>[0-9]+)', views.ReviewView.review_element, name='review_element'),
  url(r'^', views.ReviewView.review_collection, name='review_collection'),
]
