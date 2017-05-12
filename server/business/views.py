from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView

from .models import Business, BusinessBillingInfo
from .serializers import BusinessSerializer, BusinessBillingInfoSerializer
from django.shortcuts import get_object_or_404
from django.views.generic.edit import View
from rest_framework.authtoken.models import Token

@permission_classes(IsAuthenticated, )
@authentication_classes(JSONWebTokenAuthentication, )

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

	@api_view(['GET', 'POST', 'PUT'])
	def business_billing_info(request, id):
		if request.method == 'GET':
			billing_info = get_object_or_404(BusinessBillingInfo, business=id)
			serializer = BusinessBillingInfoSerializer(billing_info)
			return Response(serializer.data)
		elif request.method == 'POST':
			request.data['business_id'] = id;
			serializer = BusinessBillingInfoSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		elif request.method == 'PUT':
			billing_info = get_object_or_404(BusinessBillingInfo, business_id=id)
			serializer = BusinessBillingInfoSerializer(billing_info, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)