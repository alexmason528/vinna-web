import jwt
from rest_framework import serializers
from server.account.serializers import AccountSerializer
from .models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    business_id = serializers.IntegerField()
    cashier_account = AccountSerializer(read_only=True)
    cashier_account_id = serializers.IntegerField(write_only=True)
    qrcode = serializers.CharField(write_only=True)
    amount = serializers.FloatField()
    post_date = serializers.DateTimeField(read_only=True)
    #balance = serializers.FloatField()
    class Meta:
        model = Purchase
        fields = ('amount', 'qrcode', 'business_id', 'cashier_account_id', 'cashier_account', 'post_date')

    def create(self, validated_data):
        validated_data['account_id'] = jwt.decode(validated_data.pop('qrcode'), 'secret')['id']
        purchase = Purchase.objects.create(**validated_data)

        purchase.business_percent = 0.1;
        purchase.member_percent = 0.02;
        purchase.member_ref_percent = 0.04;

        purchase.business_amount = round(purchase.amount * purchase.business_percent,2);
        purchase.member_amount = round(purchase.amount * purchase.member_percent,2);
        purchase.member_ref_amount = round(purchase.amount * purchase.member_ref_percent,2);

        return purchase
