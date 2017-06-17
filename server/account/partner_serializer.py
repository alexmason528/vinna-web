from rest_framework import serializers
from server.account.partner_model import AccountPartnerRole
from server.business.serializers import BusinessSerializer
from server.account.serializers import AccountSerializer

class AccountPartnerRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    account_id = serializers.IntegerField(write_only=True)
    business_id = serializers.IntegerField(write_only=True)
    account = AccountSerializer(read_only=True)

    class Meta:
        model = AccountPartnerRole
        fields = ('id', 'account_id', 'account', 'business_id', 'role', 'description')