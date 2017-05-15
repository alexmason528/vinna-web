from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Customer, CreditCard, BankAccount

class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer

class CreditCardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CreditCard

class BankAccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BankAccount
