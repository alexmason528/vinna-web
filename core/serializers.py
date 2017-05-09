from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Language, Country, State

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('code','english_text','text')
