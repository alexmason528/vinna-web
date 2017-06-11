from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Country, State

class CountrySerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(read_only = True)

	class Meta:
		model = Country
		fields = ('id', 'english_text')


class StateSerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(read_only=True)
	country_id = serializers.IntegerField(read_only=True)

	class Meta:
		model = State
		fields = ('id', 'country_id', 'text')

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email')