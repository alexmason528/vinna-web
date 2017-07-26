import random

from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse

from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from server.purchase.models import Purchase
from server.account.models import Account

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

class ForgetPasswordView(APIView):
	@api_view(['POST'])
	@permission_classes([])
	@authentication_classes([])
	def forget_password(request):
		if request.method == 'POST':
			if 'email' in request.data:
				
				email = request.data['email']
				user = User.objects.get(email = email)

				if not user:
					return Response('Email does not exist', status=status.HTTP_400_BAD_REQUEST)

				code = random.randint(1000, 9999)
				
				mail_content = 'New password: ' + str(code)

				try:
					send_mail(
						'From Vinna',
						mail_content,
						'noreply@vinna.me',
						[email],
						fail_silently=False,
					)
				except Exception as e:
					return Response('Failed to send new password to your email address - ' + user.email, status=status.HTTP_400_BAD_REQUEST)

				user.password = make_password(code)
				user.save()

				return Response('Password changed', status=status.HTTP_200_OK)

			elif 'phone' in request.data:
				
				phone = request.data['phone']
				account = Account.objects.get(phone = phone)

				if not account:
					return Response('Email does not exist', status=status.HTTP_400_BAD_REQUEST)

				code = random.randint(1000, 9999)
				sms_content = 'New password: ' + str(code)
				plivo_instance = plivo.RestAPI(settings.PLIVO_AUTH_ID, settings.PLIVO_TOKEN)

				params = {
				    'src': '15612641630',
				    'dst' : account.user.email,
				    'text' : sms_content,
				    'method' : 'POST'
				}

				response = plivo_instance.send_message(params)

				if response[0] != 202:
					return Response(response[1], status=status.HTTP_400_BAD_REQUEST)

				user.password = make_password(code)
				user.save()

			return Response('Password changed', status=status.HTTP_200_OK)
