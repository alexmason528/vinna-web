import stripe
import time

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import serializers
from ipware.ip import get_real_ip, get_ip

from core.models import Country

from core.serializers import CountrySerializer, StateSerializer
from server.purchase.models import Purchase
from server.account.partner_model import AccountPartnerRole
from server.media.models import BusinessImage

from server.media.serializers import BusinessImageSerializer

from .models import Category, SubCategory, Business, BusinessBillingInfo

stripe.api_key = settings.STRIPE_API_KEY

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if data == '' and self.allow_empty_file:
            return ''

        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class SubCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    class Meta:
        model = SubCategory
        fields = ('id', 'category_id', 'text')

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(source='get_sub_categories', many=True)
    class Meta:
        model = Category
        fields = ('id', 'text', 'sub_categories')

class BusinessBillingInfoSerializer(serializers.ModelSerializer):
    business_id = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    active = serializers.BooleanField()
    address2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = BusinessBillingInfo
        fields = ('business_id', 'active', 'type', 'text', 'token', 'country_id', 'state_id', 'zip', 'address1', 'address2')

class BusinessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    billing_info = BusinessBillingInfoSerializer(write_only=True)
    account_id = serializers.IntegerField()
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    sub_category_id = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    customer_token = serializers.CharField(required=False)
    email = serializers.CharField()
    security_hash = serializers.CharField(required=False)
    ssn_token = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    current_billing_info = BusinessBillingInfoSerializer(source='get_billing_info', read_only=True)
    address2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    picture1 = Base64ImageField(max_length=None, use_url=True)
    picture2 = Base64ImageField(required=False, max_length=None, use_url=True, allow_empty_file=True, allow_null=True)
    picture3 = Base64ImageField(required=False, max_length=None, use_url=True, allow_empty_file=True, allow_null=True)
    picture4 = Base64ImageField(required=False, max_length=None, use_url=True, allow_empty_file=True, allow_null=True)

    class Meta:
        model = Business
        fields = ('id', 'account_id', 'text', 'taxid', 'country_id', 'state_id', 'city', 'zip', 'address1', 'address2','email', 'phone', 'description', 'category', 'category_id', 'sub_category_id', 'customer_token', 'security_hash', 'ssn_token', 'billing_info', 'picture1', 'picture2', 'picture3', 'picture4', 'current_billing_info', 'hours')

    def create(self, validated_data):

        country = get_object_or_404(Country, pk = validated_data['country_id'])

        customer = None

        try:
            customer = stripe.Customer.create(
                email=validated_data['email'],
                description=validated_data['description']
            )
        except stripe.error.StripeError as e:
            raise ValidationError(e.json_body['error']['message'])
        
        billing_info = validated_data.pop('billing_info')

        if customer:
            validated_data['customer_token'] = customer['id']

        business = Business.objects.create(**validated_data)
        customer.metadata = { 'Business' : business.id }

        try:
            customer.save()
        except stripe.error.StripeError as e:
            business.delete()
            customer.delete()
            raise ValidationError(e.json_body['error']['message'])

        role = AccountPartnerRole.objects.create(account_id=validated_data['account_id'], business_id=business.id, role="cashier")
        card_id = None

        try:
            response = customer.sources.create(source=billing_info['token'])
            card_id = response['id']
            customer.default_source = card_id
            customer.save()
        except stripe.error.StripeError as e:
            role.delete()
            business.delete()
            customer.delete()
            raise ValidationError(e.json_body['error']['message'])

        billing_info['token'] = card_id

        BusinessBillingInfo.objects.create(business=business, **billing_info)
        
        return business

    def update(self, instance, validated_data):
        if 'billing_info' in validated_data:
            billing_info = validated_data.pop('billing_info')
            business_billing_info = get_object_or_404(BusinessBillingInfo, business=instance)
            business_billing_info.type = billing_info['type']
            business_billing_info.text = billing_info['text']

            card_id = None
            try:
                customer = stripe.Customer.retrieve(instance.customer_token)
                response = customer.sources.create(source=billing_info['token'])
                card_id = response['id']
                customer.default_source = card_id
                customer.save()
            except stripe.error.StripeError as e:
                raise ValidationError(e.json_body['error']['message'])

            business_billing_info.token = card_id
            business_billing_info.save()

        for item in validated_data:
            if Business._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance

class BusinessPublicSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    sub_category_id = serializers.IntegerField()
    country_id = serializers.IntegerField()
    country = CountrySerializer(read_only=True)
    state_id = serializers.IntegerField()
    state = StateSerializer(read_only=True)
    email = serializers.CharField()
    description = serializers.CharField(required=False)

    picture1 = Base64ImageField(max_length=None, use_url=True)
    picture2 = Base64ImageField(max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False)
    picture3 = Base64ImageField(max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False)
    picture4 = Base64ImageField(max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False)

    class Meta:
        model = Business
        fields = ('id', 'text', 'country_id', 'country', 'state_id', 'state', 'city', 'zip', 'address1', 'address2','email', 'phone', 'description', 'category', 'sub_category_id', 'picture1', 'picture2', 'picture3', 'picture4', 'hours')

class BusinessPurchaseSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)
    business_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Purchase
        fields = ('void_date', 'amount', 'member_id', 'business_id', 'post_date', 'business_amount')

    def update(self, instance, validated_data):
        setattr(instance, 'void_date', validated_data['void_date'])
        instance.save()

        return instance
