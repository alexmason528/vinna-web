import random
import plivo

from datetime import date
from dateutil.relativedelta import relativedelta

from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from vinna.authentication import CustomJSONWebTokenAuthentication

from server.business.models import Business
from server.business.serializers import BusinessSerializer
from server.member.models import Member
from server.media.models import BusinessImage
from server.purchase.models import Purchase

from server.media.serializers import BusinessImageSerializer

from .models import Account
from .serializers import AccountSerializer

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class AccountView(APIView):

	@api_view(['GET', 'POST'])
	@permission_classes([])
	@authentication_classes([])
	@transaction.atomic
	def account_collection(request):
		if request.method == 'GET':
			accounts = Account.objects.filter(pk=request.user.id)
			serializer = AccountSerializer(accounts, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = AccountSerializer(data=request.data)
			
			if (serializer.data.id != request.user.id):
				return Response("Error.", status=status.HTTP_400_BAD_REQUEST)

			if serializer.is_valid():
				try:
					serializer.save()
				except Exception as e:
					return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['PUT','GET'])
	@transaction.atomic
	def account_element(request, id):
		# Overwrite user id with authorized user.
		id = request.user.id

		if request.method == 'GET':	
			account = get_object_or_404(Account, pk=id)
			serializer = AccountSerializer(account)
			return Response(serializer.data)

		elif request.method == 'PUT':
			account = get_object_or_404(Account, pk=id)

			if ('current_password' in request.data) and ('username' in request.data):
				credentials = {
					'username': request.data.pop('current_password'),
					'password': request.data.pop('username')
				}

				user = authenticate(**credentials)

				if not user:
					return Response('Current password is not correct', status=status.HTTP_400_BAD_REQUEST)

				request.data.pop('current_password')
				request.data.pop('username')

			serializer = AccountSerializer(account, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET'])
	def nearest_partner(request, id):
		if request.method == 'GET':
			businesses = Business.objects.filter(account_id=id).order_by('-last_modified_date')
			serializer = BusinessSerializer(businesses, many=True)

			return Response(serializer.data)

	@api_view(['GET'])
	def purchase_info(request, id):
		total_earned = Purchase.objects.filter(account_id=id).aggregate(total_earned=Coalesce(Sum('member_amount'), 0))['total_earned']
		next_payment = Purchase.objects.filter(account_id=id, member_amount_processed=0).aggregate(next_payment=Coalesce(Sum('member_amount'),0))['next_payment']
		payday = date.today().replace(day=1) + relativedelta(months=1)

		purchase_info = {
			'total_earned': total_earned,
			'next_payment': next_payment,
			'payday': payday
		}

		return Response(purchase_info)

	@api_view(['POST'])
	def verify_email(request, id):
		if request.method == 'POST':
			if 'email_code' in request.data:
				email_code = request.data['email_code']
				account = get_object_or_404(Account, pk=id)

				if account.new_email and account.new_email_verified != 1:
					if (account.new_email_verified == email_code):
						user = account.user
						user.username = account.new_email
						user.email = account.new_email
						user.save()
						
						account.email_verified = 1
						account.new_email_verified = 0
						account.new_email = ''

						account.save()

						return Response('new_email_verified', status=status.HTTP_200_OK)

				elif account.email_verified != 1:
					if account.email_verified == email_code:
						account.email_verified = 1
						account.save()

						return Response('current_email_verified', status=status.HTTP_200_OK)

				return Response('Failed to verify your email', status=status.HTTP_400_BAD_REQUEST)


	@api_view(['POST'])
	@permission_classes([])
	@authentication_classes([])	
	def find_phone(request):
		if request.method == 'POST':
			if 'phone' in request.data:
				phone = request.data['phone']
				account = get_object_or_404(Account, phone=phone)
				return Response(account.first_name, status=status.HTTP_200_OK)

			return Response('Failed to find phone 1.', status=status.HTTP_400_BAD_REQUEST)
		return Response('Failed to find phone 2.', status=status.HTTP_400_BAD_REQUEST)


	@api_view(['POST'])
	def verify_phone(request, id):
		if request.method == 'POST':
			if 'phone_code' in request.data:
				phone_code = request.data['phone_code']
				account = get_object_or_404(Account, pk=id)

				if account.new_phone and account.new_phone_verified != 1:
					if account.new_phone_verified == phone_code:
						account.phone = account.new_phone
						account.phone_verified = 1
						account.new_phone_verified = 0
						account.new_phone = ''

						account.save()

						return Response('new_phone_verified', status=status.HTTP_200_OK)

				elif account.phone_verified != 1:
					if account.phone_verified == phone_code:
						account.phone_verified = 1
						account.save()

						return Response('current_phone_verified', status=status.HTTP_200_OK)

				return Response('Failed to verify your email', status=status.HTTP_400_BAD_REQUEST)

	@api_view(['POST'])
	def update_email(request, id):
		if request.method == 'POST':
			if 'email' in request.data:
				email = request.data['email']
				account = get_object_or_404(Account, pk=id)
				account.new_email = email

				code = random.randint(1000, 9999)

				mail_content = 'Thanks for using Vinna app. \nPlease verify your email address. \nVerification code: ' + str(code)
					
				try:
					send_mail(
						'From Vinna',
						mail_content,
						settings.VERIFICATION_SENDER_EMAIL,
						[email],
						fail_silently=False,
					)
					
				except Exception as e:
					return Response('Failed to send verification code to your email - ' + account.user.email, status=status.HTTP_400_BAD_REQUEST)

				account.new_email_verified = code
				account.save()

				return Response('Email updated', status=status.HTTP_200_OK)

	@api_view(['POST'])
	def update_phone(request, id):
		if request.method == 'POST':
			if 'phone' in request.data:
				phone = request.data['phone']
				account = get_object_or_404(Account, pk=id)
				account.new_phone = phone

				code = random.randint(1000, 9999)

				sms_content = 'Thanks for using Vinna app. \nPlease verify your phone number. \nVerification code: ' + str(code)
				plivo_instance = plivo.RestAPI(settings.PLIVO_AUTH_ID, settings.PLIVO_TOKEN)
				
				params = {
				    'src': settings.VERIFICATION_SENDER_PHONE,
				    'dst' : phone,
				    'text' : sms_content,
				    'method' : 'POST'
				}

				response = plivo_instance.send_message(params)

				if response[0] != 202:
					return Response(response[1], status=status.HTTP_400_BAD_REQUEST)

				account.new_phone_verified = code
				account.save()

				return Response('Phone updated', status=status.HTTP_200_OK)
				

	@api_view(['GET'])
	def send_email_code(request, id):
		if request.method == 'GET':
			account = get_object_or_404(Account, pk=id)
			code = random.randint(1000, 9999)

			if account.email_verified == 1:
				return Response('Email is already verified', status=status.HTTP_400_BAD_REQUEST)

			mail_content = 'Thanks for using Vinna app. \nPlease verify your email address. \nVerification code: ' + str(code)
			
			try:
				send_mail(
					'From Vinna',
					mail_content,
					settings.VERIFICATION_SENDER_EMAIL,
					[account.user.email],
					fail_silently=False,
				)
				
			except Exception as e:
				return Response('Failed to send verification code to your email - ' + account.user.email, status=status.HTTP_400_BAD_REQUEST)

			account.email_verified = code
			account.save()

			return Response('Code updated', status=status.HTTP_200_OK)

	@api_view(['GET'])
	def send_phone_code(request, id):
		if request.method == 'GET':
			account = get_object_or_404(Account, pk=id)
			code = random.randint(1000, 9999)

			if account.phone_verified == 1:
				return Response('Phone is already verified', status=status.HTTP_400_BAD_REQUEST)

			sms_content = 'Thanks for using Vinna app. \nPlease verify your phone number. \nVerification code: ' + str(code)
			plivo_instance = plivo.RestAPI(settings.PLIVO_AUTH_ID, settings.PLIVO_TOKEN)
			
			account = get_object_or_404(Account, pk=id)

			params = {
			    'src': settings.VERIFICATION_SENDER_PHONE,
			    'dst' : account.phone,
			    'text' : sms_content,
			    'method' : 'POST'
			}

			response = plivo_instance.send_message(params)

			if response[0] != 202:
				return Response(response[1], status=status.HTTP_400_BAD_REQUEST)

			account.phone_verified = code
			account.save()

			return Response('Code updated', status=status.HTTP_200_OK)
