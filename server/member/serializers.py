import stripe
import jwt
import time


from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from ipware.ip import get_real_ip, get_ip

from core.models import Country

from server.purchase.models import Purchase
from server.account.models import Account

from .models import Member, MemberPaymentInfo

stripe.api_key = settings.STRIPE_API_KEY

class MemberPaymentInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    member_id = serializers.IntegerField(required=False)

    class Meta:
        model = MemberPaymentInfo
        fields = ('id', 'member_id', 'text', 'token', 'routing_number')

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    account_id = serializers.IntegerField()
    mailing_address_state_id = serializers.IntegerField()
    mailing_address_country_id = serializers.IntegerField()
    managed_account_token = serializers.CharField(required=False)
    payment_infos = MemberPaymentInfoSerializer(required=False, many=True)
    registration_link = serializers.CharField(source='get_registration_link', read_only=True)
    security_hash = serializers.CharField(required=False)
    ssn_token = serializers.CharField(required=False)
    mailing_address_2 = serializers.CharField(required=False)

    class Meta:
        model = Member
        fields = ('id', 'account_id', 'mailing_address_1','mailing_address_2','mailing_address_city', 'mailing_address_state_id', 'mailing_address_zip', 'mailing_address_country_id', 'managed_account_token', 'security_hash', 'ssn_token','payment_infos', 'registration_link')

    def create(self, validated_data):
        account = get_object_or_404(Account, pk=validated_data['account_id'])
        email = account.user.email

        country = get_object_or_404(Country, pk=validated_data['mailing_address_country_id'])

        response = stripe.Account.create(
            type = 'custom',
            email = email,
            country = country.abbrev
        )

        validated_data['managed_account_token'] = response['id']

        payment_infos, referral_link = None, None

        if 'payment_infos' in validated_data:
            payment_infos = validated_data.pop('payment_infos')

        member = Member.objects.create(**validated_data)

        stripe_account = stripe.Account.retrieve(response['id'])
        stripe_account.legal_entity.dob.year = account.dob.year
        stripe_account.legal_entity.dob.day = account.dob.day
        stripe_account.legal_entity.dob.month = account.dob.month
        stripe_account.legal_entity.business_name = account.first_name + ' ' + account.last_name
        stripe_account.legal_entity.type = 'individual'
        stripe_account.legal_entity.address = stripe_account.legal_entity.personal_address = {
            'city': member.mailing_address_city,
            'country': member.mailing_address_country.abbrev,
            'line1': member.mailing_address_1,
            'line2': member.mailing_address_2,
            'postal_code': member.mailing_address_zip,
            'state': member.mailing_address_state.abbrev
        }

        stripe_account.legal_entity.first_name = account.first_name
        stripe_account.legal_entity.last_name = account.last_name
        stripe_account.legal_entity.personal_id_number = member.ssn_token
        stripe_account.tos_acceptance.date = str(time.time()).split('.')[0]
        stripe_account.tos_acceptance.ip = get_ip(self.context['request'])
        
        stripe_account.metadata = { 'Member' : member.id }
        stripe_account.save()

        if payment_infos is not None:
            for payment_info in payment_infos:
                MemberPaymentInfo.objects.create(member=member, **payment_info)

        return member

    def update(self, instance, validated_data):
        if 'referral_link' in validated_data:
            validated_data.pop('referral_link')

        if 'payment_infos' in validated_data:
            validated_data.pop('payment_infos')

        for item in validated_data:
            if Member._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance


class MemberPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
