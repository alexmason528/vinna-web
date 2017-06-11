from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Image, Video, BusinessImage, BusinessVideo

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('hash', 's3_url', 'title', 'description')

class BusinessImageSerializer(ImageSerializer):
    business_id = serializers.IntegerField(required=True)
    class Meta:
        model = BusinessImage
        fields = ('business_id', 'hash', 's3_url', 'title', 'description', 'created_at')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('link', 'unique_code', 'platform')

class BusinessVideoSerializer(VideoSerializer):
    business_id = serializers.IntegerField(required=True)
    class Meta:
        model = BusinessVideo
        fields = ('business_id', 'link', 'unique_code', 'platform')
