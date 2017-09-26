from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Purchase
from .serializers import ViewPurchaseSerializer, NewPurchaseSerializer

class PurchaseView(APIView):

	@api_view(['POST'])
	def purchase_collection(request):
		if request.method == 'POST':
			serializer = NewPurchaseSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['GET', 'POST'])
	def business_purchase_collection(request, business_id):
		if request.method == 'GET':
			purchases = Purchase.objects.filter(business_id=business_id).filter(business_account_id=request.user.id)
			serializer = ViewPurchaseSerializer(purchases, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = NewPurchaseSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET'])
	def purchase_element(request, id):
		purchase = get_object_or_404(Purchase, pk=id)
		if request.user.account.id != purchase.account.id:
			raise PermissionDenied

		if request.method == 'GET':		
			serializer = ViewPurchaseSerializer(purchase)
			return Response(serializer.data)

		elif request.method == 'PUT':
			serializer = NewPurchaseSerializer(purchase, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				raise ValidationError(detail={'error': serializer.errors})
