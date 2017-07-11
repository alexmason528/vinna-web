from datetime import date
from dateutil.relativedelta import relativedelta

from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from vinna.authentication import CustomJSONWebTokenAuthentication

from server.business.models import Business
from server.business.serializers import BusinessSerializer
from server.media.models import BusinessImage
from server.purchase.models import Purchase

from server.media.serializers import BusinessImageSerializer

from .models import Account
from .serializers import AccountSerializer

class AccountView(APIView):

	@api_view(['GET', 'POST'])
	@permission_classes([])
	@authentication_classes([])
	@transaction.atomic
	def account_collection(request):
		if request.method == 'GET':
			accounts = Account.objects.all()
			serializer = AccountSerializer(accounts, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = AccountSerializer(data=request.data)
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
					return Response('Current password is wrong', status=status.HTTP_400_BAD_REQUEST)

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
			
			for business in serializer.data:
				business_image = BusinessImage.objects.filter(business_id=business['id']).order_by('-created_at').first()
				business_image_serializer = BusinessImageSerializer(business_image)
				business['image'] = business_image_serializer.data

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

