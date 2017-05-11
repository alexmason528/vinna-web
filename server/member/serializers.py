from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Member, MemberPaymentInfo

class MemberPaymentInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MemberPaymentInfo
        fields = ('type', 'text', 'token')

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    payment_infos = MemberPaymentInfoSerializer(required=False, many=True)
    account_id = serializers.IntegerField(required=True)
    mailing_address_state_id = serializers.IntegerField(required=True)
    mailing_address_country_id = serializers.IntegerField(required=True)

    class Meta:
        model = Member
        fields = ('account_id', 'mailing_address_1','mailing_address_2','mailing_address_city', 'mailing_address_state_id', 'mailing_address_zip', 'mailing_address_country_id', 'security_hash', 'ssn_token', 'payment_infos')

    def create(self, validated_data):
        payment_infos = None
        if 'payment_infos' in validated_data:
            payment_infos = validated_data.pop('payment_infos')

        member = Member.objects.create(**validated_data)

        if payment_infos is not None:
            for payment_info in payment_infos:
                MemberPaymentInfo.objects.create(member=member, **payment_info)

        return member

    def update(self, instance, validated_data):
        instance.mailing_address_1 = validated_data.get('mailing_address_1', instance.mailing_address_1)
        instance.mailing_address_2 = validated_data.get('mailing_address_2', instance.mailing_address_2)
        instance.mailing_address_city = validated_data.get('mailing_address_city', instance.mailing_address_city)
        instance.mailing_address_state = validated_data.get('mailing_address_state', instance.mailing_address_state)
        instance.mailing_address_zip = validated_data.get('mailing_address_zip', instance.mailing_address_zip)
        instance.mailing_address_country = validated_data.get('mailing_address_country', instance.mailing_address_country)
        instance.security_hash = validated_data.get('security_hash', instance.security_hash)
        instance.ssn_token = validated_data.get('ssn_token', instance.ssn_token)

        instance.save()

        return instance
