import hashlib
import string

from rest_framework import serializers
from server.media.serializers import BusinessImageSerializer
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    link = serializers.CharField(required=False)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    account_id = serializers.IntegerField(required=False)
    business_id = serializers.IntegerField()

    pic1 = serializers.CharField(write_only=True)
    pic2 = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    pic3 = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    pic4 = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = Notification
        fields = ('title', 'category', 'message', 'state', 'link', 'start', 'end', 'account_id', 'business_id', 'pic1', 'pic2', 'pic3', 'pic4')

    def create(self, validated_data):
        pic1 = pic2 = pic3 = pic4 = None

        if 'pic1' in validated_data:
            pic1 = validated_data.pop('pic1')
        if 'pic2' in validated_data:
            pic2 = validated_data.pop('pic2')
        if 'pic3' in validated_data:
            pic3 = validated_data.pop('pic3')
        if 'pic4' in validated_data:
            pic4 = validated_data.pop('pic4')

        notification = Notification.objects.create(**validated_data)
        if pic1:
            serializer = BusinessImageSerializer(data={
                'business_id': notification.business.id,
                'hash': hashlib.md5(pic1.encode('utf-8')).hexdigest(),
                's3_url': pic1,
                'type': 'Notification'
            })
            if serializer.is_valid():
                serializer.save()

        if pic2:
            serializer = BusinessImageSerializer(data={
                'business_id': notification.business.id,
                'hash': hashlib.md5(pic2.encode('utf-8')).hexdigest(),
                's3_url': pic2,
                'type': 'Notification'
            })
            if serializer.is_valid():
                serializer.save()

        if pic3:
            serializer = BusinessImageSerializer(data={
                'business_id': notification.business.id,
                'hash': hashlib.md5(pic3.encode('utf-8')).hexdigest(),
                's3_url': pic3,
                'type': 'Notification'
            })
            if serializer.is_valid():
                serializer.save()

        if pic4:
            serializer = BusinessImageSerializer(data={
                'business_id': notification.business.id,
                'hash': hashlib.md5(pic4.encode('utf-8')).hexdigest(),
                's3_url': pic4,
                'type': 'Notification'
            })
            if serializer.is_valid():
                serializer.save()

        return notification