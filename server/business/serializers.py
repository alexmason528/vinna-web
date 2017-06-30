import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from core.models import Country

from server.purchase.models import Purchase
from server.account.partner_model import AccountPartnerRole
from server.media.models import BusinessImage

from server.media.serializers import BusinessImageSerializer

from .models import Category, SubCategory, Business, BusinessBillingInfo

stripe.api_key = settings.STRIPE_API_KEY

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'text')

class SubCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    class Meta:
        model = SubCategory
        fields = ('category_id', 'text')

class BusinessBillingInfoSerializer(serializers.ModelSerializer):
    business_id = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    active = serializers.BooleanField()

    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2')

class BusinessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    billing_info = BusinessBillingInfoSerializer(required=False)
    account_id = serializers.IntegerField()
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    sub_category_id = serializers.IntegerField()
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    managed_account_token = serializers.CharField(required=False)
    email = serializers.EmailField()
    security_hash = serializers.CharField(required=False)
    ssn_token = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    images = BusinessImageSerializer(source='get_images', many=True)
    class Meta:
        model = Business
        fields = ('id', 'account_id', 'text', 'taxid', 'country_id', 'state_id', 'city', 'zip', 'address1', 'address2','email', 'phone', 'description', 'category', 'category_id', 'sub_category_id', 'managed_account_token', 'security_hash', 'ssn_token', 'billing_info', 'images')

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

        account = stripe.Account.retrieve(response['id'])
        account.metadata = { 'Business' : business.id }
        account.save()

        AccountPartnerRole.objects.create(account_id=validated_data['account_id'], business_id=business.id, role="cashier")

        if billing_info is not None:
            extAccountResponse = account.external_accounts.create(external_account=billing_info['token'])
            billing_info['token'] = extAccountResponse['id']
            BusinessBillingInfo.objects.create(business=business, **billing_info)

        return business

    def update(self, instance, validated_data):

        billing_info = None
        if 'billing_info' in validated_data:
            billing_info = validated_data.pop('billing_info')
        business_billing_info = get_object_or_404(BusinessBillingInfo, business=instance)
        business_billing_info.type = billing_info['type']
        business_billing_info.text = billing_info['text']

        account = stripe.Account.retrieve(instance.managed_account_token)
        extAccountResponse = account.external_accounts.create(external_account=billing_info['token'])
        business_billing_info.token = extAccountResponse['id']

        business_billing_info.save()

        for item in validated_data:
            if Business._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance

class BusinessPurchaseSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)
    business_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Purchase
        fields = ('void_date', 'amount', 'member_id', 'business_id')

    def update(self, instance, validated_data):
        setattr(instance, 'void_date', validated_data['void_date'])
        instance.save()

        return instance
