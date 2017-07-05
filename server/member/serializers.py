import stripe
import jwt

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers

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

    class Meta:
        model = Member
        fields = ('id', 'account_id', 'mailing_address_1','mailing_address_2','mailing_address_city', 'mailing_address_state_id', 'mailing_address_zip', 'mailing_address_country_id', 'managed_account_token', 'security_hash', 'ssn_token','payment_infos', 'registration_link')

    def create(self, validated_data):
        account = get_object_or_404(Account, pk=validated_data['account_id'])
        email = account.user.email

        country = get_object_or_404(Country, pk=validated_data['mailing_address_country_id'])

        response = stripe.Account.create(
            managed=True,
            email = email,
            country = country.abbrev
        )

        validated_data['managed_account_token'] = response['id']

        payment_infos, referral_link = None, None

        if 'payment_infos' in validated_data:
            payment_infos = validated_data.pop('payment_infos')

        member = Member.objects.create(**validated_data)

        account = stripe.Account.retrieve(response['id'])
        account.metadata = { 'Member' : member.id }
        account.save()

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
