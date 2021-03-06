import plivo
import random

from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from server.business.models import Business
from server.member.models import Member
from server.media.models import BusinessImage
from server.purchase.models import Purchase

from server.business.serializers import BusinessSerializer
from server.media.serializers import BusinessImageSerializer
from server.purchase.serializers import ViewPurchaseSerializer

from .models import Account
from .serializers import AccountSerializer

class AccountView(APIView):

	@api_view(['POST'])
	@permission_classes([])
	@authentication_classes([])
	@transaction.atomic
	def account_collection(request):
		if request.method == 'POST':
			serializer = AccountSerializer(data=request.data)
			
			if serializer.is_valid():
				try:
					serializer.save()
				except Exception as e:
					raise ValidationError(detail={'error': str(e)})

				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET'])
	@transaction.atomic
	def account_element(request, id):
		if request.user.account.id != int(id):
			raise PermissionDenied

		if request.method == 'GET':
			account = get_object_or_404(Account, pk=id)
			serializer = AccountSerializer(account)
			return Response(serializer.data, status=status.HTTP_200_OK)

		elif request.method == 'PUT':
			account = get_object_or_404(Account, pk=id)
			serializer = AccountSerializer(account, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['GET'])
	def nearest_partner(request, id):
		if request.user.account.id != int(id):
			raise PermissionDenied

		if request.method == 'GET':
			account = get_object_or_404(Account, pk=id)
			businesses = Business.objects.filter(account_id=id).order_by('-last_modified_date')
			serializer = BusinessSerializer(businesses, many=True)

			return Response(serializer.data, status=status.HTTP_200_OK)

	# Summary
	@api_view(['GET'])
	def purchase_info(request, id):
		if request.method == 'GET':
			if request.user.account.id != int(id):
				raise PermissionDenied

			total_earned = Purchase.objects.filter(account_id=id).aggregate(total_earned=Coalesce(Sum('member_amount'), 0))['total_earned']
			next_payment = Purchase.objects.filter(account_id=id, member_amount_processed=0).aggregate(next_payment=Coalesce(Sum('member_amount'),0))['next_payment']
			payday = date.today().replace(day=1) + relativedelta(months=1)

			purchase_info = {
				'total_earned': total_earned,
				'next_payment': next_payment,
				'payday': payday
			}

			return Response(purchase_info, status=status.HTTP_200_OK)

	@api_view(['GET'])
	def purchase_collection(request, id):
		if request.method == 'GET':
			if request.user.account.id != int(id):
				raise PermissionDenied

			purchases = Purchase.objects.filter(account_id=id)
			serializer = ViewPurchaseSerializer(purchases, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)


	@api_view(['POST'])
	def verify_email(request, id):
		if request.method == 'POST':
			if request.user.account.id != int(id):
				raise PermissionDenied

			if not 'email_code' in request.data:
				raise ValidationError(detail={'error': 'Email code is required'})

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

			raise ValidationError(detail={'error': 'Failed to verify your email'})

	@api_view(['POST'])
	def verify_phone(request, id):
		if request.method == 'POST':
			if request.user.account.id != int(id):
				raise PermissionDenied

			if not 'phone_code' in request.data:
				raise ValidationError(detail={'error': 'Phone verification code is required'})

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

			raise ValidationError(detail={'error': 'Failed to verify your phone'})

	@api_view(['POST'])
	def update_email(request, id):
		if request.method == 'POST':
			if request.user.account.id != int(id):
				raise PermissionDenied

			if not 'email' in request.data:
				raise ValidationError(detail={'error': 'Email is required'})

			email = request.data['email']

			if User.objects.filter(username=email).count() > 0:
				raise ValidationError(detail={'error': 'This email is already taken by other account'})

			account = get_object_or_404(Account, pk=id)
			account.new_email = email

			code = random.randint(1000, 9999)

			mail_content = '''Thanks for using Vinna app.
			Please verify your email address. 
			Verification code: %d''' % code

			try:
				send_mail(
					'From Vinna',
					mail_content,
					settings.VERIFICATION_SENDER_EMAIL,
					[email],
					fail_silently=False,
				)
				
			except Exception as e:
				raise ValidationError(detail={'error': 'Failed to send verification code to your email'})

			account.new_email_verified = code
			account.save()

			return Response('Email updated', status=status.HTTP_200_OK)

	@api_view(['POST'])
	def update_phone(request, id):
		if request.method == 'POST':
			if request.user.account.id != int(id):
				raise PermissionDenied

			if not 'phone' in request.data:
				raise ValidationError(detail={'error': 'Phone number is required'})

			phone = request.data['phone']

			if Account.objects.filter(phone=phone).count() > 0:
				raise ValidationError(detail={'error': 'Phone number is already taken by other account'})

			account = get_object_or_404(Account, pk=id)
			account.new_phone = phone

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
				raise ValidationError(detail={'error': response[1]})

			account.new_phone_verified = code
			account.save()

			return Response({'detail': 'Phone updated'}, status=status.HTTP_200_OK)
				

	@api_view(['GET'])
	def send_email_code(request, id):
		if request.method == 'GET':
			if request.user.account.id != int(id):
				raise PermissionDenied

			account = get_object_or_404(Account, pk=id)
			code = random.randint(1000, 9999)

			if account.email_verified == 1:
				raise ValidationError(detail={'error': 'Email is already verified'})

			mail_content = '''Thanks for using Vinna app.
				Please verify your email address.
				Verification code: %d''' % code
			
			try:
				send_mail(
					'From Vinna',
					mail_content,
					settings.VERIFICATION_SENDER_EMAIL,
					[account.user.email],
					fail_silently=False,
				)
				
			except Exception as e:
				raise ValidationError(detail={'error': 'Failed to send verificatio code to your email'})

			account.email_verified = code
			account.save()

			return Response({'detail': 'Code updated'}, status=status.HTTP_200_OK)

	@api_view(['GET'])
	def send_phone_code(request, id):
		if request.method == 'GET':
			if request.user.account.id != int(id):
				raise PermissionDenied

			account = get_object_or_404(Account, pk=id)
			code = random.randint(1000, 9999)

			if account.phone_verified == 1:
				raise ValidationError(detail={'error': 'This email is already verified'})

			sms_content = '''Thanks for using Vinna app.
			Please verify your phone number.
			Verification code: %d''' % code
			
			plivo_instance = plivo.RestAPI(settings.PLIVO_AUTH_ID, settings.PLIVO_TOKEN)
			
			account = get_object_or_404(Account, pk=id)

			params = {
			    'src': settings.VERIFICATION_SENDER_PHONE,
			    'dst' : account.country.phone_country_code + account.phone,
			    'text' : sms_content,
			    'method' : 'POST'
			}

			response = plivo_instance.send_message(params)

			if response[0] != 202:
				raise ValidationError(detail={'error': response[1]})

			account.phone_verified = code
			account.save()

			return Response({'detail': 'Code updated'}, status=status.HTTP_200_OK)

	@api_view(['POST'])
	@permission_classes([])
	@authentication_classes([])	
	def find_phone(request):
		if request.method == 'POST':
			if not 'phone' in request.data:
				raise ValidationError(detail={'error': 'Phone number is required'})

			phone = request.data['phone']

			account = None
			try:
				account = get_object_or_404(Account, phone=phone)
			except:
				pass

			if account:
				return Response(account.first_name, status=status.HTTP_200_OK)
			else:
				code = random.randint(1000, 9999)

				sms_content = 'Vinna code: ' + str(code)
				plivo_instance = plivo.RestAPI(settings.PLIVO_AUTH_ID, settings.PLIVO_TOKEN)
				
				params = {
				    'src': settings.VERIFICATION_SENDER_PHONE,
				    'dst' : '1' + phone,
				    'text' : sms_content,
				    'method' : 'POST'
				}
				response = plivo_instance.send_message(params)

				raise ValidationError(detail={code})

	@api_view(['POST'])
	@permission_classes([])
	@authentication_classes([])
	def find_email(request):
		if request.method == 'POST':
			if not 'email' in request.data:
				raise ValidationError(detail={'error': 'Email is required'})

			email = request.data['email'].lower()
			account = get_object_or_404(User, email=email)
			return Response(account.first_name, status=status.HTTP_200_OK)
