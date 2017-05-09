from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    phone = serializers.CharField(required=True, max_length=10)
    gender = serializers.CharField(required=False, max_length=1)

    class Meta:
        model = Account
        fields = ('first_name','last_name','phone','dob','gender','profile_photo_url') #,'language')

        extra_kwargs = {
#            'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
            'language': {'view_name':'language-detail', 'lookup_field': 'code'}
        }

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
