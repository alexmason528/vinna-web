from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView

from .models import Country, State, Language
from .serializers import CountrySerializer, StateSerializer, LanguageSerializer
from django.shortcuts import get_object_or_404
from django.views.generic.edit import View
from rest_framework.authtoken.models import Token


# @permission_classes((IsAuthenticated,))

class CountryView(APIView):

	@api_view(['GET', 'POST'])
	def country_collection(request):
		if request.method == 'GET':
			countries = Country.objects.all()
			serializer = CountrySerializer(countries, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = CountrySerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['PUT','GET'])
	def country_element(request, countryid):
		if request.method == 'GET':	
			country = get_object_or_404(Country, pk=countryid)
			serializer = CountrySerializer(country)
			return Response(serializer.data)

		elif request.method == 'PUT':
			country = get_object_or_404(Country, pk=countryid)
			serializer = CountrySerializer(country, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateView(APIView):

	@api_view(['GET', 'POST'])
	def state_collection(request):
		if request.method == 'GET':
			states = State.objects.all()
			serializer = StateSerializer(states, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = StateSerializer(data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['PUT','GET'])
	def state_element(request, stateid):
		if request.method == 'GET':	
			state = get_object_or_404(State, pk=stateid)
			serializer = StateSerializer(state)
			return Response(serializer.data)

		elif request.method == 'PUT':
			state = get_object_or_404(State, pk=stateid)
			serializer = StateSerializer(state, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageView(APIView):

	@api_view(['GET', 'POST'])
	def language_collection(request):
		if request.method == 'GET':
			languages = Language.objects.all()
			serializer = LanguageSerializer(languages, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = LanguageSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['PUT','GET'])
	def language_element(request, languageid):
		if request.method == 'GET':	
			language = get_object_or_404(Language, pk=languageid)
			serializer = LanguageSerializer(language)
			return Response(serializer.data)

		elif request.method == 'PUT':
			language = get_object_or_404(Language, pk=languageid)
			serializer = LanguageSerializer(language, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)