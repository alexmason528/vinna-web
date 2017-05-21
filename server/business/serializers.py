import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Category, SubCategory, Business, BusinessBillingInfo
from core.serializers import StripeManagedAccountSerializer, StripeBankAccountSerializer, StripeCreditCardSerializer

stripe.api_key = settings.STRIPE_API_KEY

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('text')

class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.IntegerField()
    class Meta:
        model = SubCategory
        fields = ('category_id', 'text')

class BusinessBillingInfoSerializer(serializers.HyperlinkedModelSerializer):
    country_id = serializers.IntegerField(read_only=True)
    state_id = serializers.IntegerField(read_only=True)
    business_id = serializers.IntegerField(read_only=True)
    token = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2')

class BusinessBillingBankInfoSerializer(BusinessBillingInfoSerializer):
    account_info = StripeCreditCardSerializer(required=False)
    token = serializers.CharField(required=False)

    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2', 'account_info')

    def create(self, validated_data):
        account_info, response = None, None
        if 'account_info' in validated_data:
            account_info = validated_data.pop('account_info')

        business = get_object_or_404(Business, pk=validated_data['business_id'])
        managed_account = stripe.Account.retrieve(business.managed_account_token)

        if account_info is not None:
            account_info['external_account']['object'] = 'bank_account'
            response = managed_account.external_accounts.create(
                external_account = account_info['external_account']
            )
        if response is not None:
            validated_data['token'] = response['id']

        validated_data['type'] = 'bank'
        
        member_payment_info = MemberPaymentInfo.create(**validated_data)

        return member_payment_info

    def update(self, instance, validated_data):

        account_info,response = None, None
        if 'account_info' in validated_data:
            account_info = validated_data.pop('account_info')

        business = get_object_or_404(Business, pk=validated_data['business_id'])
        managed_account = stripe.Account.retrieve(business.managed_account_token)

        if account_info is not None:
            account_info['external_account']['object'] = 'bank_account'
            response = managed_account.external_accounts.create(
                external_account = account_info['external_account']
            )

        if response is not None:
            if instance.token is not None:
                card_account = managed_account.external_accounts.retrieve(instance.token)
                card_account.delete()
            setattr(instance, 'token', response['id'])
            
        for item in validated_data:
            if BusinessBillingInfo._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance


class BusinessBillingCreditInfoSerializer(BusinessBillingInfoSerializer):
    account_info = StripeCreditCardSerializer(required=False)
    token = serializers.CharField(required=False)

    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2', 'account_info')

    def create(self, validated_data):
        account_info, response = None, None
        if 'account_info' in validated_data:
            account_info = validated_data.pop('account_info')

        business = get_object_or_404(Business, pk=validated_data['business_id'])
        managed_account = stripe.Account.retrieve(business.managed_account_token)

        if account_info is not None:
            account_info['external_account']['object'] = 'card'
            response = managed_account.external_accounts.create(
                external_account = account_info['external_account']
            )
        if response is not None:
            validated_data['token'] = response['id']

        validated_data['type'] = 'card'
        
        member_payment_info = MemberPaymentInfo.create(**validated_data)

        return member_payment_info

    def update(self, instance, validated_data):

        account_info,response = None, None
        if 'account_info' in validated_data:
            account_info = validated_data.pop('account_info')

        business = get_object_or_404(Business, pk=validated_data['business_id'])
        managed_account = stripe.Account.retrieve(business.managed_account_token)

        if account_info is not None:
            account_info['external_account']['object'] = 'card'
            response = managed_account.external_accounts.create(
                external_account = account_info['external_account']
            )

        if response is not None:
            if instance.token is not None:
                card_account = managed_account.external_accounts.retrieve(instance.token)
                card_account.delete()
            setattr(instance, 'token', response['id'])
            
        for item in validated_data:
            if BusinessBillingInfo._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance


class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    billing_info = BusinessBillingInfoSerializer(required=False)
    account_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    sub_category_id = serializers.IntegerField()
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    stripe_account_info = StripeManagedAccountSerializer(required=False)
    managed_account_token = serializers.CharField(required=False)
    email = serializers.EmailField()

    class Meta:
        model = Business
        fields = ('account_id', 'text', 'taxid', 'country_id', 'state_id', 'zip', 'address1', 'address2','email', 'phone', 'category_id', 'sub_category_id', 'managed_account_token', 'security_hash', 'ssn_token', 'stripe_account_info', 'billing_info')

    def create(self, validated_data):

        sa_info, response = None, None
        if 'stripe_account_info' in validated_data:
            sa_info = validated_data.pop('stripe_account_info')

        if sa_info is not None:
            response = stripe.Account.create(
                managed=True,
                email=sa_info['email']
            )

        billing_info = None
        if 'billing_info' in validated_data:
            billing_info = validated_data.pop('billing_info')

        if response is not None:
            validated_data['managed_account_token'] = response['id']

        business = Business.objects.create(**validated_data)
        if billing_info is not None:
            BusinessBillingInfo.objects.create(business=business, **billing_info)

        return business

    def update(self, instance, validated_data):
        sa_info,response = None, None
        if 'stripe_account_info' in validated_data:
            sa_info = validated_data.pop('stripe_account_info')

        if sa_info is not None:
            response = stripe.Account.create(
                managed=True,
                email=sa_info['email']
            )

        if response is not None:
            if instance.managed_account_token is not None:
                account = stripe.Account.retrieve(instance.managed_account_token)
                account.delete()
            setattr(instance, 'managed_account_token', response['id'])

            
        for item in validated_data:
            if Business._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance
