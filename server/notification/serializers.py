from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Notification
        fields = ('title', 'category', 'message')