from rest_framework import serializers

class StripeBankAccountExternalAccountSerializer(serializers.Serializer):
	account_number = serializers.IntegerField()
	country = serializers.CharField(max_length=3)
	currency = serializers.CharField(max_length=7)
	account_holder_name = serializers.CharField(max_length=50, required=False)
	account_holder_type = serializers.ChoiceField(choices=['individual', 'company'], required=False)
	routing_number = serializers.CharField()

class StripeCreditCardExternalAccountSerializer(serializers.Serializer):
	exp_month = serializers.IntegerField()
	exp_year = serializers.IntegerField()
	number = serializers.IntegerField()
	address_city = serializers.CharField(max_length=20, required=False)
	address_country = serializers.CharField(max_length=20, required=False)
	address_line1 = serializers.CharField(max_length=30, required=False)
	address_line2 = serializers.CharField(max_length=30, required=False)
	address_zip = serializers.CharField(max_length=10, required=False)
	currency = serializers.CharField(max_length=3)
	cvc = serializers.CharField(max_length=10)
	default_for_currency = serializers.BooleanField()
	metadata = serializers.DictField(required=False)
	name = serializers.CharField(max_length=20, required=False)

class StripeManagedAccountSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=3, required=False)
    email = serializers.EmailField()

class StripeBankAccountSerializer(serializers.Serializer):
	external_account = StripeBankAccountExternalAccountSerializer()
	default_for_currenty = serializers.BooleanField(required=False)
	metadata = serializers.DictField(required=False)

class StripeCreditCardSerializer(serializers.Serializer):
	external_account = StripeCreditCardExternalAccountSerializer()
	default_for_currency = serializers.BooleanField(required=False)
	metadata = serializers.DictField(required=False)