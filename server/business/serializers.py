import stripe
import time
from ipware.ip import get_real_ip, get_ip

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
    images = BusinessImageSerializer(source='get_images', many=True, read_only=True)
    class Meta:
        model = Business
        fields = ('id', 'account_id', 'text', 'taxid', 'country_id', 'state_id', 'city', 'zip', 'address1', 'address2','email', 'phone', 'description', 'category', 'category_id', 'sub_category_id', 'managed_account_token', 'security_hash', 'ssn_token', 'billing_info', 'images')

    def create(self, validated_data):
        country = get_object_or_404(Country, pk = validated_data['country_id'])

        response = None
        response = stripe.Account.create(
            type='custom',
            email=validated_data['email'],
            country=country.abbrev
        )

        validated_data['sub_category_id'] = 1
        
        billing_info = None
        if 'billing_info' in validated_data:
            billing_info = validated_data.pop('billing_info')

        if response is not None:
            validated_data['managed_account_token'] = response['id']

        business = Business.objects.create(**validated_data)

        stripe_account = stripe.Account.retrieve(response['id'])
        stripe_account.legal_entity.dob.year = business.account.dob.year
        stripe_account.legal_entity.dob.day = business.account.dob.day
        stripe_account.legal_entity.dob.month = business.account.dob.month
        stripe_account.legal_entity.business_name = business.account.first_name + ' ' + business.account.last_name
        stripe_account.legal_entity.type = 'individual'
        stripe_account.legal_entity.address = stripe_account.legal_entity.personal_address = {
            'city': business.city,
            'country': business.country.abbrev,
            'line1': business.address1,
            'line2': business.address2,
            'postal_code': business.zip,
            'state': business.state.abbrev
        }

        stripe_account.legal_entity.first_name = business.account.first_name
        stripe_account.legal_entity.last_name = business.account.last_name
        stripe_account.legal_entity.personal_id_number = business.ssn_token
        stripe_account.tos_acceptance.date = str(time.time()).split('.')[0]
        stripe_account.tos_acceptance.ip = get_ip(self.context['request'])
        stripe_account.metadata = { 'Business' : business.id }
#        stripe_account.save()

        AccountPartnerRole.objects.create(account_id=validated_data['account_id'], business_id=business.id, role="cashier")

        if billing_info is not None:
#            extAccountResponse = stripe_account.external_accounts.create(external_account=billing_info['token'])
#            billing_info['token'] = extAccountResponse['id']
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
