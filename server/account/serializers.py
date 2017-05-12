from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Account, AccountPartnerRole

class AccountPartnerRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountPartnerRole
        fields = ('role_name', 'role_description')

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    roles = AccountPartnerRoleSerializer(many=True, required=False)
    user_id = serializers.IntegerField(required=True)
    language_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Account
        fields = ('user_id', 'first_name','last_name', 'language_id', 'phone', 'dob', 'gender', 'profile_photo_url', 'roles')

    def create(self, validated_data):
        roles = None
        if 'roles' in validated_data:
            roles = validated_data.pop('roles')

        account = Account.objects.create(**validated_data)

        if roles is not None:
            for role in roles:
                AccountPartnerRole.objects.create(account=account, **role)

        return account

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.profile_photo_url = validated_data.get('profile_photo_url', instance.profile_photo_url)

        instance.save()

        return instance
