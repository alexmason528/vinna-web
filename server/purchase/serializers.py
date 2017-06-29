from rest_framework import serializers
from .models import Purchase
from server.account.serializers import AccountSerializer

class PurchaseSerializer(serializers.ModelSerializer):
    cashier_account = AccountSerializer(read_only=True)
    cashier_account_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Purchase
        fields = ('amount','cashier_account', 'cashier_account_id', 'post_date', 'balance')
