from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


from . import views

app_name = 'media'

urlpatterns = [
    url(r'^image/(?P<id>[0-9]+)', views.ImageView.image_element, name='image_element'),
    url(r'^image', views.ImageView.image_collection, name='image_collection'),
    url(r'^video/(?P<id>[0-9]+)', views.VideoView.video_element, name='video_element'),
    url(r'^video', views.VideoView.video_collection, name='video_collection'),
    url(r'^bimage/(?P<id>[0-9]+)', views.BusinessImageView.business_image_element, name='business_image_element'),
    url(r'^bimage', views.BusinessImageView.business_image_collection, name='business_image_collection'),
    url(r'^bvideo/(?P<id>[0-9]+)', views.BusinessVideoView.business_video_element, name='business_video_element'),
    url(r'^bvideo', views.BusinessVideoView.business_video_collection, name='business_video_collection'),
]
