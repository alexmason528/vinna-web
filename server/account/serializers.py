from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Account, Role, AccountRole
from django.shortcuts import get_object_or_404

class AccountRoleSerializer(serializers.HyperlinkedModelSerializer):
    role_id = serializers.ReadOnlyField(source='role.id')
    account_id = serializers.ReadOnlyField(source='account.id')

    class Meta:
        model = AccountRole
        fields = ('role_id', 'account_id')

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description')

class AccountListSerializer(serializers.HyperlinkedModelSerializer):
    roles = RoleSerializer(many=True)
    user_id = serializers.IntegerField()
    language_id = serializers.IntegerField()

    class Meta:
        model = Account
        fields = ('user_id', 'first_name','last_name', 'language_id', 'phone', 'dob', 'gender', 'profile_photo_url', 'roles')

class AccountCreateSerializer(serializers.HyperlinkedModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(many=True, write_only=True, required=False, queryset = Role.objects.all())
    user_id = serializers.IntegerField()
    language_id = serializers.IntegerField()

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
                AccountRole.objects.create(account=account, role=role)
        return account

    def update(self, instance, validated_data):
        roles = None
        if 'roles' in validated_data:
            roles = validated_data.pop('roles')
        for item in validated_data:
            if Account._meta.get_field(item):
                setattr(instance, item, validated_data[item])

        if roles is not None:
            AccountRole.objects.filter(account=instance).delete()
            for role in roles:
                AccountRole.objects.create(account=instance, role=role)
        instance.save()
        return instance
