from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Account, AccountPartnerRole, AccountPartnerRoleList

class AccountPartnerRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountPartnerRole
        fields = ('id', 'role_name', 'role_description')

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.IntegerField(required=True)
    language_id = serializers.IntegerField(required=True)
    partner_roles = AccountPartnerRoleSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('user_id', 'first_name','last_name', 'language_id', 'phone', 'dob', 'gender', 'profile_photo_url', 'partner_roles')

    # def create(self, validated_data):
    #     roles = None
    #     if 'partner_roles' in validated_data:
    #         roles = validated_data.pop('partner_roles')

    #     account = Account.objects.create(**validated_data)
    #     if roles is not None:
    #         for role in roles:
    #             pr = get_object_or_404(AccountPartnerRole, pk=roles['id'])
    #             account.partner_role.add(pr)

    #     return account

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.dob = validated_data.get('dob', instance.dob)
    #     instance.gender = validated_data.get('gender', instance.gender)
    #     instance.profile_photo_url = validated_data.get('profile_photo_url', instance.profile_photo_url)


    #     instance.save()

    #     return instance

class AccountPartnerRoleListSerializer(serializers.HyperlinkedModelSerializer):
    account_id = serializers.ReadOnlyField(source='account.id')
    accountpartnerrole_id = serializers.ReadOnlyField(source='partner_role.id')

    class Meta:
        model = AccountPartnerRoleList
        fields = ('account_id', 'accountpartnerrole_id')

