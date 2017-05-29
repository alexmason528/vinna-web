import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from core.serializers import StripeManagedAccountSerializer
from server.purchase.models import Purchase
from core.models import Country

from .models import Category, SubCategory, Business, BusinessBillingInfo

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
    business_id = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    active = serializers.BooleanField()

    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2')

class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    billing_info = BusinessBillingInfoSerializer(required=False)
    account_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    sub_category_id = serializers.IntegerField()
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    managed_account_token = serializers.CharField(required=False)
    email = serializers.EmailField()
    security_hash = serializers.CharField(required=False)
    ssn_token = serializers.CharField(required=False)

    class Meta:
        model = Business
        fields = ('account_id', 'text', 'taxid', 'country_id', 'state_id', 'zip', 'address1', 'address2','email', 'phone', 'category_id', 'sub_category_id', 'managed_account_token', 'security_hash', 'ssn_token', 'billing_info')

    def create(self, validated_data):
        country = get_object_or_404(Country, pk = validated_data['country_id'])

        response = None
        response = stripe.Account.create(
            managed=True,
            email=validated_data['email'],
            country=country.abbrev
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
        for item in validated_data:
            if Business._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance

class BusinessPurchaseSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(write_only=True)
    business_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Purchase
        fields = ('void_date', 'amount', 'member_id', 'business_id')

    def update(self, instance, validated_data):
        setattr(instance, 'void_date', validated_data['void_date'])
        instance.save()

        return instance
