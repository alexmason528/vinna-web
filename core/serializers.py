from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Country, State


class StateSerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(read_only=True)
	country_id = serializers.IntegerField(read_only=True)

	class Meta:
		model = State
		fields = ('id', 'country_id', 'text')

class CountrySerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(read_only = True)
	states = StateSerializer(source='get_states', many=True)

	class Meta:
		model = Country
		fields = ('id', 'english_text', 'states')


class UserSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	first_name = serializers.CharField(write_only=True)
	last_name = serializers.CharField(write_only=True)
	is_superuser = serializers.CharField(write_only=True)
	is_staff = serializers.CharField(write_only=True)
	is_active = serializers.CharField(write_only=True)
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'username', 'is_superuser', 'is_staff', 'is_active', 'email', 'password')
