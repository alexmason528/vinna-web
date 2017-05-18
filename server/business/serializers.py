import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Category, SubCategory, Business, BusinessBillingInfo
from core.serializers import StripeManagedAccountSerializer, StripeBankAccountSerializer

# import datetime

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
    account_info = serializers.DictField(write_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2', 'account_info')

    def create(self, validated_data):
        account_info = validated_data.pop('account_info')

        business = get_object_or_404(Business, pk=validated_data['business_id'])
        managed_account = stripe.Account.retrieve(business.managed_account_token)

        # response = None
        ba_info['external_account']['object'] = 'bank_account'

        # response = managed_account.external_accounts.create(
        #     external_account = ba_info['external_account']
        # )

        validated_data['type'] = 'bank'
        validated_data['token'] = '12345'
        member_payment_info = MemberPaymentInfo.create(**validated_data)

        return member_payment_info

class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    billing_info = BusinessBillingInfoSerializer(read_only=True)
    account_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    sub_category_id = serializers.IntegerField()
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    stripe_account_info = StripeManagedAccountSerializer(write_only=True)
    managed_account_token = serializers.CharField(read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Business
        fields = ('account_id', 'text', 'taxid', 'country_id', 'state_id', 'zip', 'address1', 'address2','email', 'phone', 'category_id', 'sub_category_id', 'managed_account_token', 'security_hash', 'ssn_token', 'stripe_account_info', 'billing_info')

    def create(self, validated_data):
        sa_info = validated_data.pop('stripe_account_info')

        response = stripe.Account.create(
            managed=True,
            email=sa_info['email']
        )

        billing_info = None

        if 'billing_info' in validated_data:
            billing_info = validated_data.pop('billing_info')

        validated_data['managed_account_token'] = response['id']

        business = Business.objects.create(**validated_data)

        if billing_info is not None:
            BusinessBillingInfo.objects.create(business=business, **billing_info)

        return business

    def update(self, instance, validated_data):

        sa_info = None
        if 'stripe_account_info' in validated_data:
            sa_info = validated_data.pop('stripe_account_info')
            
        for item in validated_data:
            if Business._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance
