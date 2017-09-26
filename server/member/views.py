
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from server.purchase.models import Purchase
from .models import Member, MemberPaymentInfo
from .serializers import MemberSerializer, MemberPaymentInfoSerializer, MemberPurchaseSerializer

class MemberView(APIView):

	@api_view(['GET', 'POST'])
	@transaction.atomic
	def member_collection(request):
		if request.method == 'GET':
			members = Member.objects.all()
			serializer = MemberSerializer(members, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = MemberSerializer(data=request.data, context={'request': request})
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
	def member_element(request, id):
		if request.method == 'GET':	
			member = get_object_or_404(Member, pk=id)
			serializer = MemberSerializer(member)
			return Response(serializer.data, status=status.HTTP_200_OK)

		elif request.method == 'PUT':
			member = get_object_or_404(Member, pk=id)
			serializer = MemberSerializer(member, data=request.data, partial=True)

			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				raise ValidationError(detail={'error': serializer.errors})

class MemberPaymentInfoView(APIView):

	@api_view(['GET', 'POST'])
	@transaction.atomic
	def member_payment_info_collection(request, id):
		if request.method == 'GET':
			member_payment_infos = MemberPaymentInfo.objects.filter(member_id = id)
			serializer = MemberPaymentInfoSerializer(member_payment_infos, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		
		elif request.method == 'POST':
			request.data['member_id'] = id
			serializer = MemberPaymentInfoSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET', 'DELETE'])
	@transaction.atomic
	def member_payment_info_element(request, id, pinfo_id):
		if request.method == 'GET':	
			member_payment_info = get_object_or_404(MemberPaymentInfo, pk=pinfo_id)
			serializer = MemberPaymentInfoSerializer(member_payment_info)
			return Response(serializer.data, status=status.HTTP_200_OK)

		elif request.method == 'PUT':
			member_payment_info = get_object_or_404(MemberPaymentInfo, pk=pinfo_id)
			serializer = MemberPaymentInfoSerializer(member_payment_info, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			member_payment_info = get_object_or_404(MemberPaymentInfo, pk=pinfo_id)
			member_payment_info.delete()

class MemberPurchaseView(APIView):
	@api_view(['GET'])
	def member_purchase_collection(request, id):
		if request.method == 'GET':
			purchases = Purchase.objects.filter(Q(member_id=id) | Q(member_referral_id=id))
			serializer = MemberPurchaseSerializer(purchases, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

	@api_view(['GET'])
	def member_purchase_element(request, id, purchase_id):
		purchase = get_object_or_404(Purchase, pk=purchase_id)
		serializer = MemberPurchaseSerializer(purchase)
		return Response(serializer.data, status=status.HTTP_200_OK)
