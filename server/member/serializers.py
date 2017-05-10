from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Member, MemberPaymentInfo

class MemberPaymentInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountPartnerRole
        fields = ('type', 'text', 'token')

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    roles = AccountPartnerRoleSerializer(many=True, required=False)

    class Meta:
        model = Account
        fields = ('mailing_address_1','mailing_address_2','phone', 'dob', 'gender', 'profile_photo_url', 'roles')

        # extra_kwargs = {
        #     'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
        #     'language': {'view_name':'language-detail', 'lookup_field': 'code'}
        # }

    def create(self, validated_data):
        roles = None
        if 'roles' in validated_data:
            roles = validated_data.pop('roles')

        account = Account.objects.create(**validated_data)

        if 'roles' is not None:
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
