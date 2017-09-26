from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from server.account.models import Account
from server.account.partner_model import AccountPartnerRole
from server.media.models import BusinessImage
from server.purchase.models import Purchase

from server.account.partner_serializer import AccountPartnerRoleSerializer
from server.media.serializers import BusinessImageSerializer

from .models import Business, BusinessBillingInfo, Category
from .invitation_model import Invitation
from .serializers import BusinessSerializer, BusinessPublicSerializer, BusinessBillingInfoSerializer, BusinessPurchaseSerializer, CategorySerializer
from .invitation_serializer import InvitationSerializer

class BusinessView(APIView):

	@api_view(['GET', 'POST'])
	@transaction.atomic
	@permission_classes([])
	@authentication_classes([])
	def business_collection(request):
		if request.method == 'GET':
			businesses = Business.objects.all().order_by('-last_modified_date')
			serializer = BusinessPublicSerializer(businesses, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = BusinessSerializer(data=request.data, context={'request': request})
			if serializer.is_valid():
				try:
					serializer.save()
				except Exception as e:
					raise ValidationError(detail={'error': str(e)})

				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET'])
	def business_element(request, id):
		if request.user.account.business_set.all().filter(id=id).count() == 0:
			raise PermissionDenied

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
				raise ValidationError(detail={'error': serializer.errors})

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
			else:
				raise ValidationError(detail={'error': serializer.errors})

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
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			biling_info = get_object_or_404(BusinessBillingInfo, pk=binfo_id)
			billing_info.delete()

class BusinessPurchaseView(APIView):
	@api_view(['GET'])
	def business_purchase_summary(request, id):
		if request.method == 'GET':
			purchase_aggregate = Purchase.objects.filter(business_id = id).aggregate(total_sales=Coalesce(Sum('member_amount'), 0), total_customers=Coalesce(Count('member_amount'), 0))
#			payday = date.today().replace(day=1) + relativedelta(months=1)

#			b_purchases = Purchase.objects.filter(business_id = id).filter(business__account__id = request.user.id)

			purchase_summary = {
				'total_sales': purchase_aggregate['total_sales'],
				'total_customers': purchase_aggregate['total_customers'],
#				'purchases': b_purchases
			}

			return Response(purchase_summary)

	@api_view(['GET', 'POST'])
	def business_purchase_collection(request, id):
		if request.method == 'GET':
			b_purchases = Purchase.objects.filter(business_id = id).filter(business__account__id = request.user.id)
			serializer = BusinessPurchaseSerializer(b_purchases, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			request.data['business_id'] = id
			serializer = BusinessPurchaseSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

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
				raise ValidationError(detail={'error': serializer.errors})

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
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['GET'])
	def business_invitation_element(request, id, invitation_id):
		if request.method == 'GET':	
			invitation = get_object_or_404(Invitation, pk=invitation_id)
			serializer = InvitationSerializer(invitation)
			return Response(serializer.data)

class BusinessCashierView(APIView):

	@api_view(['GET', 'POST'])
	def business_cashier_purchase_summary(request, id):
		if request.method == 'GET':
			return;

	@api_view(['GET', 'POST'])
	@transaction.atomic
	def business_cashier_collection(request, id):
		if request.method == 'GET':
			business = Business.objects.get(pk=id)
			cashiers = AccountPartnerRole.objects.filter(business=business).exclude(account=business.account)
			serializer = AccountPartnerRoleSerializer(cashiers, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

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
						raise ValidationError(detail={'error': str(e)})

					return Response(serializer.data, status=status.HTTP_201_CREATED)
				else:
					raise ValidationError(detail={'error': serializer.errors})

			else:
				account = Account.objects.get(user_id=user.id)
				partner_role_data = {
					'account_id': account.id,
					'business_id': id,
					'role': 'cashier',
					'description': 'extra'
				}

				if AccountPartnerRole.objects.filter(business_id = id, account_id = account.id).count() > 0:
					raise ValidationError(detail={'error': 'You already added this user as your cashier'})

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
			return Response(serializer.data, status=status.HTTP_200_OK)
