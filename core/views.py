import random
import plivo

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
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from server.purchase.models import Purchase
from server.account.models import Account

from vinna.authentication import CustomJSONWebTokenAuthentication

from .models import Country, State
from .serializers import CountrySerializer, StateSerializer


@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class Version():
	
	@api_view(['GET'])
	@permission_classes([])
	@authentication_classes([])
	def version_info(request, platform):
		if request.method == 'GET':
			if platform == 'ios':
				version_info = {
					'version': 1.1,
					'supported': [0.98, 0.95, 0.90],
					'public_stripe': 'pk_test_vSXaN8PlxDIA9SRDrvPyNllu'
				}
				return Response(version_info, status=status.HTTP_200_OK)
			elif platform == 'android':
				version_info = {
					'version': 1.1,
					'supported': [0.98, 0.95, 0.90],
					'public_stripe': 'pk_test_vSXaN8PlxDIA9SRDrvPyNllu'
				}
				return Response(version_info, status=status.HTTP_200_OK)
			else:
				return Response('Unsupported platform', status=status.HTTP_400_BAD_REQUEST)
		
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
				
				mail_content = 'Reset code to change your password: ' + str(code)

				try:
					send_mail(
						'From Vinna',
						mail_content,
						settings.VERIFICATION_SENDER_EMAIL,
						[email],
						fail_silently=False,
					)
				except Exception as e:
					return Response('Failed to send reset code to your email address - ' + email, status=status.HTTP_400_BAD_REQUEST)

				return Response(code, status=status.HTTP_200_OK)

			elif 'phone' in request.data:
				print(request.data['phone'])
				phone = request.data['phone']
				account = Account.objects.get(phone = phone)

				if not account:
					return Response('Phone number does not exist', status=status.HTTP_400_BAD_REQUEST)

				code = random.randint(1000, 9999)
				sms_content = 'Vinna code: ' + str(code)
				plivo_instance = plivo.RestAPI(settings.PLIVO_AUTH_ID, settings.PLIVO_TOKEN)

				params = {
			    'src': settings.VERIFICATION_SENDER_PHONE,
			    'dst' : account.country.phone_country_code + phone,
			    'text' : sms_content,
			    'method' : 'POST'
				}

				response = plivo_instance.send_message(params)

				if response[0] != 202:
					print(response[1])
					return Response('Failed to send reset code to your phone -' + str(phone), status=status.HTTP_400_BAD_REQUEST)
				elif response[0] == 202:
					return Response(code, status=status.HTTP_200_OK)

			return Response('Failed to send reset code', status=status.HTTP_400_BAD_REQUEST)

	@api_view(['POST'])
	@permission_classes([])
	@authentication_classes([])		
	def reset_password(request):
		if request.method == 'POST':
			phone = request.data['phone']
			password = request.data['password']

			account = get_object_or_404(Account, phone=phone)
			user = account.user
			user.password = make_password(password)
			user.save()

			return Response('Password changed', status=status.HTTP_200_OK)
