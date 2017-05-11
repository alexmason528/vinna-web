from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Language, Country, State

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    code = serializers.CharField(required=False)
    english_text = serializers.CharField(required=False)
    text = serializers.CharField(required=False)

    class Meta:
        model = Language
        fields = ('id', 'code', 'english_text', 'text')

class StateSerializer(serializers.HyperlinkedModelSerializer):
    language_id = serializers.IntegerField(required=True)
    country_id = serializers.IntegerField(required=True)

    class Meta:
        model = State
        fields = ('id', 'abbrev', 'text', 'language_id', 'country_id')

    def create(self, validated_data):
        language_id = validated_data.pop('language_id')
        country_id = validated_data.pop('country_id')

        language = Language.objects.get(pk=language_id)
        country = Country.objects.get(pk=country_id)

        state = State.objects.create(language=language, country=country, **validated_data)
        return state

    def update(self, instance, validated_data):
        instance.abbrev = validated_data.get('abbrev', instance.abbrev)
        instance.text = validated_data.get('text', instance.text)
        instance.language_id = validated_data.get('language_id', instance.language_id)
        instance.country_id = validated_data.get('country_id', instance.country_id)

        instance.save()

        return instance       

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    states = StateSerializer(required=False, many=True)
    default_language = LanguageSerializer(required=True)

    class Meta:
        model = Country
        fields = ('id', 'phone_country_code','abbrev','text', 'english_text', 'states', 'default_language')

    def create(self, validated_data):
        states = None

        dl = validated_data.pop('default_language')
        default_language = Language.objects.get(pk=dl['id'])

        if 'states' in validated_data:
            states = validated_data.pop('states')

        country = Country.objects.create(default_language=default_language, **validated_data)

        if states is not None:
            for state in states:
                State.objects.create(country=country, **state)

        return country

    def update(self, instance, validated_data):

        instance.phone_country_code = validated_data.get('phone_country_code', instance.phone_country_code)

        instance.abbrev = validated_data.get('abbrev', instance.abbrev)
        instance.text = validated_data.get('text', instance.text)
        instance.english_text = validated_data.get('english_text', instance.text)
        instance.default_language = Language.objects.get(pk=validated_data.get('default_language')['id'])

        instance.save

        return instance