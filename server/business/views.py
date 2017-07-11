from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from vinna.authentication import CustomJSONWebTokenAuthentication

from server.purchase.models import Purchase
from server.media.models import BusinessImage
from server.account.models import Account
from server.account.partner_model import AccountPartnerRole
from .models import Business, BusinessBillingInfo, Category
from .invitation_model import Invitation

from server.media.serializers import BusinessImageSerializer
from server.account.partner_serializer import AccountPartnerRoleSerializer
from .serializers import BusinessSerializer, BusinessBillingInfoSerializer, BusinessPurchaseSerializer, CategorySerializer
from .invitation_serializer import InvitationSerializer


@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class BusinessView(APIView):

	@api_view(['GET', 'POST'])
	@transaction.atomic
	def business_collection(request):
		if request.method == 'GET':
			businesses = Business.objects.all().order_by('-last_modified_date')
			serializer = BusinessSerializer(businesses, many=True)

			return Response(serializer.data)
		
		elif request.method == 'POST':

			serializer = BusinessSerializer(data=request.data, context={'request': request})
			
			if serializer.is_valid():
				try:
					serializer.save()
				except Exception as e:
					return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	@api_view(['PUT','GET'])
	def business_element(request, id):
		if request.method == 'GET':	
			business = get_object_or_404(Business, pk=id)
			serializer = BusinessSerializer(business)
			return Response(serializer.data)

		elif request.method == 'PUT':
			business = get_object_or_404(Business, pk=id)
			serializer = BusinessSerializer(business, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET'])
	def category(request):
		if request.method == 'GET':
			categories = Category.objects.all()
			serializer = CategorySerializer(categories, many=True)

			return Response(serializer.data)

class BusinessBillingInfoView(APIView):

	@api_view(['GET', 'POST'])
	def business_billing_info_collection(request, id):
		if request.method == 'GET':
			billing_infos = BusinessBillingInfo.objects.filter(business_id=id)
			serializer = BusinessBillingInfoSerializer(billing_infos, many=True)
			return Response(serializer.data)
		elif request.method == 'POST':
			request.data['business_id'] = id
			serializer = BusinessBillingInfoSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET', 'PUT', 'DELETE'])
	def business_billing_info_element(request, id, binfo_id):
		if request.method == 'GET':
			billing_info = get_object_or_404(BusinessBillingInfo, pk=binfo_id)
			serializer = BusinessBillingInfoSerializer(billing_info)
			return Response(serializer.data)
		elif request.method == 'PUT':
			request.data['business_id'] = id
			billing_info = get_object_or_404(BusinessBillingInfo, pk=binfo_id)

			serializer = BusinessBillingInfoSerializer(billing_info, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		elif request.method == 'DELETE':
			biling_info = get_object_or_404(BusinessBillingInfo, pk=binfo_id)
			billing_info.delete()

class BusinessPurchaseView(APIView):
	
	@api_view(['GET', 'POST'])
	def business_purchase_collection(request, id):
		if request.method == 'GET':
			b_purchases = Purchase.objects.filter(business_id = id)
			serializer = BusinessPurchaseSerializer(b_purchases, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			request.data['business_id'] = id
			serializer = BusinessPurchaseSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET', 'PUT'])
	def business_purchase_element(request, id, purchase_id):
		if request.method == 'GET':	
			purchase = get_object_or_404(Purchase, pk=purchase_id)
			serializer = BusinessPurchaseSerializer(purchase)
			return Response(serializer.data)

		elif request.method == 'PUT':
			purchase = get_object_or_404(Purchase, pk=purchase_id)
			serializer = BusinessPurchaseSerializer(purchase, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessInvitationView(APIView):

	@api_view(['GET', 'POST'])
	def business_invitation_collection(request, id):
		if request.method == 'GET':
			invitations = Invitation.objects.all()
			serializer = InvitationSerializer(invitations, many=True)
			
			return Response(serializer.data)
		
		elif request.method == 'POST':
			request.data['business_id'] = id
			serializer = InvitationSerializer(data=request.data)

			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET'])
	def business_invitation_element(request, id, invitation_id):
		if request.method == 'GET':	
			invitation = get_object_or_404(Invitation, pk=invitation_id)
			serializer = InvitationSerializer(invitation)
			return Response(serializer.data)

class BusinessCashierView(APIView):

	@api_view(['GET', 'POST'])
	@transaction.atomic
	def business_cashier_collection(request, id):
		if request.method == 'GET':
			cashiers = AccountPartnerRole.objects.filter(business_id = id)
			serializer = AccountPartnerRoleSerializer(cashiers, many=True)
			return Response(serializer.data)
		if request.method == 'POST':
			user = None
			try:
				user = User.objects.get(username=request.data['email'])
			except:
				pass

			if not user:
				serializer = InvitationSerializer(data={'business_id': id, 'email': request.data['email'], 'type': 'cashier'})
				if serializer.is_valid():
					try:
						serializer.save()
					except Exception as e:
						return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

					return Response(serializer.data, status=status.HTTP_201_CREATED)
				else:
					return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			else:
				account = Account.objects.get(user_id=user.id)
				partner_role_data = {
					'account_id': account.id,
					'business_id': id,
					'role': 'cashier',
					'description': 'extra'
				}

				if AccountPartnerRole.objects.filter(business_id = id, account_id = account.id).count() > 0:
					return Response('You already added this user as your cashier', status=status.HTTP_400_BAD_REQUEST)

				AccountPartnerRole.objects.create(**partner_role_data)

				cashiers = AccountPartnerRole.objects.filter(business_id=id)
				serializer = AccountPartnerRoleSerializer(cashiers, many=True)

				return Response(serializer.data, status=status.HTTP_201_CREATED)

	@api_view(['GET', 'DELETE'])
	@transaction.atomic
	def business_cashier_element(request, id, cashier_id):
		if request.method == 'GET':
			cashier = get_object_or_404(AccountPartnerRole, pk = cashier_id)
			serializer = AccountPartnerRoleSerializer(cashier)
			return Response(serializer.data)
		elif request.method == 'DELETE':
			cashier = get_object_or_404(AccountPartnerRole, pk = cashier_id)
			cashier.delete()

			cashiers = AccountPartnerRole.objects.filter(business_id = id)
			serializer = AccountPartnerRoleSerializer(cashiers, many=True)
			return Response(serializer.data)
