import stripe
import jwt

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from .models import Member, MemberPaymentInfo
from server.purchase.models import Purchase
from server.account.models import Account

from server.account.serializers import AccountListSerializer

stripe.api_key = settings.STRIPE_API_KEY

class MemberPaymentInfoSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(required=False)
    type = serializers.CharField()
    text = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        model = MemberPaymentInfo
        fields = ('member_id', 'type', 'text', 'token')

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    account_id = serializers.IntegerField()
    mailing_address_state_id = serializers.IntegerField()
    mailing_address_country_id = serializers.IntegerField()
    managed_account_token = serializers.CharField(read_only=True)
    payment_infos = MemberPaymentInfoSerializer(write_only=True, many=True)
    registration_link = serializers.CharField(source='get_registration_link', read_only=True)
    referral_link = serializers.CharField(required=False)
    security_hash = serializers.CharField(required=False)
    ssn_token = serializers.CharField(required=False)

    class Meta:
        model = Member
        fields = ('account_id', 'mailing_address_1','mailing_address_2','mailing_address_city', 'mailing_address_state_id', 'mailing_address_zip', 'mailing_address_country_id', 'managed_account_token', 'security_hash', 'ssn_token','payment_infos', 'registration_link', 'referral_link')

    def create(self, validated_data):
        # account = AccountListSerializer(get_object_or_404(Account, pk=validated_data['account_id']))

        response = stripe.Account.create(
            managed=True
        )

        validated_data['managed_account_token'] = response['id']

        payment_infos, referral_link = None, None

        if 'payment_infos' in validated_data:
            payment_infos = validated_data.pop('payment_infos')

        if 'referral_link' in validated_data:
            referral_link = validated_data.pop('referral_link')

        if referral_link is not None:
            decoded = jwt.decode(referral_link, 'secret')
            validated_data['referral_id'] = decoded['id']

        member = Member.objects.create(**validated_data)

        if payment_infos is not None:
            for payment_info in payment_infos:
                MemberPaymentInfo.objects.create(member=member, **payment_info)

        return member

    def update(self, instance, validated_data):
        if 'referral_link' in validated_data:
            validated_data.pop('referral_link')

        sa_info = None
        if 'stripe_account_info' in validated_data:
            sa_info = validated_data.pop('stripe_account_info')

        for item in validated_data:
            if Member._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance


class MemberPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
