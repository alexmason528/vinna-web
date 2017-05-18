import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from .models import Member, MemberPaymentInfo
from core.serializers import StripeManagedAccountSerializer, StripeBankAccountSerializer

stripe.api_key = settings.STRIPE_API_KEY

class MemberPaymentInfoSerializer(serializers.HyperlinkedModelSerializer):
    bankaccount_info = StripeBankAccountSerializer(write_only=True)
    token = serializers.CharField(read_only=True)
    member_id = serializers.IntegerField(required=True)

    class Meta:
        model = MemberPaymentInfo
        fields = ('member_id', 'type', 'text', 'token', 'bankaccount_info')

    def create(self, validated_data):
        ba_info = validated_data.pop('bankaccount_info')

        member = get_object_or_404(Member, pk=validated_data['member_id'])
        managed_account = stripe.Account.retrieve(member.managed_account_token)

        response = None
        ba_info['external_account']['object'] = 'bank_account'

        response = managed_account.external_accounts.create(
            external_account = ba_info['external_account']
        )

        validated_data['token'] = response['id']
        member_payment_info = MemberPaymentInfo.create(**validated_data)

        return member_payment_info

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    payment_infos = MemberPaymentInfoSerializer(required=False, many=True)
    account_id = serializers.IntegerField(required=True)
    mailing_address_state_id = serializers.IntegerField(required=True)
    mailing_address_country_id = serializers.IntegerField(required=True)
    stripe_account_info = StripeManagedAccountSerializer(write_only=True)
    managed_account_token = serializers.CharField(read_only=True)

    class Meta:
        model = Member
        fields = ('account_id', 'mailing_address_1','mailing_address_2','mailing_address_city', 'mailing_address_state_id', 'mailing_address_zip', 'mailing_address_country_id', 'managed_account_token', 'security_hash', 'ssn_token', 'stripe_account_info', 'payment_infos')

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

        if response is not None:
            validated_data['managed_account_token'] = response['id']

        payment_infos = None
        if 'payment_infos' in validated_data:
            payment_infos = validated_data.pop('payment_infos')

        member = Member.objects.create(**validated_data)

        if payment_infos is not None:
            for payment_info in payment_infos:
                MemberPaymentInfo.objects.create(member=member, **payment_info)

        return member

    # def update(self, instance, validated_data):
    #     instance.mailing_address_1 = validated_data.get('mailing_address_1', instance.mailing_address_1)
    #     instance.mailing_address_2 = validated_data.get('mailing_address_2', instance.mailing_address_2)
    #     instance.mailing_address_city = validated_data.get('mailing_address_city', instance.mailing_address_city)
    #     instance.mailing_address_state = validated_data.get('mailing_address_state', instance.mailing_address_state)
    #     instance.mailing_address_zip = validated_data.get('mailing_address_zip', instance.mailing_address_zip)
    #     instance.mailing_address_country = validated_data.get('mailing_address_country', instance.mailing_address_country)
    #     instance.security_hash = validated_data.get('security_hash', instance.security_hash)
    #     instance.ssn_token = validated_data.get('ssn_token', instance.ssn_token)

    #     instance.save()

    #     return instance
