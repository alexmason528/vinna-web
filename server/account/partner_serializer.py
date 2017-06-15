from rest_framework import serializers
from server.account.partner_model import AccountPartnerRole

class AccountPartnerRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    account_id = serializers.IntegerField(read_only=True)
    business_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AccountPartnerRole
        fields = ('id', 'account_id', 'business_id', 'role', 'description')
