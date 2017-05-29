from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from vinna.authentication import CustomJSONWebTokenAuthentication

from .models import Business, BusinessBillingInfo
from .serializers import BusinessSerializer, BusinessBillingInfoSerializer, BusinessPurchaseSerializer
from server.purchase.models import Purchase

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class BusinessView(APIView):

	@api_view(['GET', 'POST'])
	def business_collection(request):
		if request.method == 'GET':
			businesses = Business.objects.all()
			serializer = BusinessSerializer(businesses, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = BusinessSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
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
