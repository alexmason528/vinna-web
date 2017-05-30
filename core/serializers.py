from rest_framework import serializers

from .models import Country, State

class StripeManagedAccountSerializer(serializers.HyperlinkedModelSerializer):
    country = serializers.CharField(max_length=3, required=False)
    email = serializers.EmailField(required=True)

class CountrySerializer(serializers.HyperlinkedModelSerializer):

	id = serializers.IntegerField(read_only = True)

	class Meta:
		model = Country
		fields = ('id', 'abbrev', 'english_text', 'text')


class StateSerializer(serializers.HyperlinkedModelSerializer):

	id = serializers.IntegerField(read_only=True)
	country_id = serializers.IntegerField(read_only=True)

	class Meta:
		model = State
		fields = ('id', 'country_id', 'abbrev', 'text')