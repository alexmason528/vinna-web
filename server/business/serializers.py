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
    category_id = serializers.IntegerField(required=True)
    class Meta:
        model = SubCategory
        fields = ('category_id', 'text')

class BusinessBillingInfoSerializer(serializers.HyperlinkedModelSerializer):
    country_id = serializers.IntegerField(required=True)
    state_id = serializers.IntegerField(required=True)
    business_id = serializers.IntegerField(required=True)
    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2')

class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    billing_info = BusinessBillingInfoSerializer(required=False)
    account_id = serializers.IntegerField(required=True)
    category_id = serializers.IntegerField(required=True)
    sub_category_id = serializers.IntegerField(required=True)
    country_id = serializers.IntegerField(required=True)
    state_id = serializers.IntegerField(required=True)
    stripe_account_info = StripeManagedAccountSerializer(write_only=True, required=True)
    managed_account_token = serializers.CharField(read_only=True)

    class Meta:
        model = Business
        fields = ('account_id', 'text', 'taxid', 'country_id', 'state_id', 'zip', 'address1', 'address2','email', 'phone', 'category_id', 'sub_category_id', 'managed_account_token', 'security_hash', 'ssn_token', 'stripe_account_info', 'billing_info')

    def create(self, validated_data):
        sa_info = validated_data.pop('stripe_account_info')

        response = None
        try:
            response = stripe.Account.create(
                managed=True,
                email=sa_info['email']
            )
        except Exception as e:
            pass

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
        instance.account_id = validated_data.get('account_id', instance.account_id)
        instance.text = validated_data.get('text', instance.text)
        instance.taxid = validated_data.get('taxid', instance.taxid)
        instance.country_id = validated_data.get('country_id', instance.country_id)
        instance.state_id = validated_data.get('state_id', instance.state_id)
        instance.zip = validated_data.get('zip', instance.zip)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.sub_category_id = validated_data.get('sub_category_id', instance.sub_category_id)
        instance.security_hash = validated_data.get('security_hash', instance.security_hash)
        instance.ssn_token = validated_data.get('ssn_token', instance.ssn_token)
        
        instance.save()

        return instance
