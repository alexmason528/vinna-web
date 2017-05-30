from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse

from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from server.purchase.models import Purchase

from vinna.authentication import CustomJSONWebTokenAuthentication

from .models import Country, State
from .serializers import CountrySerializer, StateSerializer


@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class CountryView(APIView):

	@api_view(['GET'])
	def country_collection(request):
		if request.method == 'GET':
			countries = Country.objects.all()
			serializer = CountrySerializer(countries, many=True)
			print(serializer.data)
			return Response(serializer.data)

	@api_view(['GET'])
	def country_element(request, country_id):
		if request.method == 'GET':	
			country = get_object_or_404(Country, pk=country_id)
			serializer = CountrySerializer(country)
			return Response(serializer.data)

class StateView(APIView):

	@api_view(['GET'])
	def state_collection(request, country_id):
		if request.method == 'GET':
			states = State.objects.filter(country_id=country_id)
			serializer = StateSerializer(states, many=True)
			return Response(serializer.data)

	@api_view(['GET'])
	def state_element(request, country_id, state_id):
		if request.method == 'GET':
			state = get_object_or_404(State, pk=state_id)
			serializer = StateSerializer(state)
			return Response(serializer.data)